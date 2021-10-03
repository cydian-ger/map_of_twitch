import concurrent.futures
import concurrent.futures.thread
import json
import random
import requests
from lxml.html import fromstring
from tqdm import tqdm
from viewer_handling.get_viewers import get_viewers

HEADERS = {'client-id': 'kimne78kx3ncx6brgo4mv6wki5h1ko'}
GQL_QUERY = """
query($login: String) {
    user(login: $login) {
        stream {
            id
        }
    }
}
"""
TIMOUT_TIME = 15
MAX_WORKERS = 256


def is_live(streamer_name: str, proxies: [str], throw_error=False) -> tuple:
    # https://www.gkbrk.com/2020/12/twitch-graphql/
    streamer_name = streamer_name.lower()
    proxy = None
    if proxies is not None:
        proxy_choice = random.choice(proxies)
        proxy = {"http://": proxy_choice, "https://": proxy_choice}

    QUERY = {
        'query': GQL_QUERY,
        'variables': {
            'login': streamer_name
        }
    }

    try:
        # Gods please have mercy
        # A problem arises when a user doesnt exists
        # For the sole reason that then the ['data']['user']['stream'] function fails without exception
        # DONT TAKE AWAY TIMEOUT OR DEATH (symptom: stops at the last 20 or sth, it seems to clog up in the futures)
        answer = requests.post('https://gql.twitch.tv/gql',
                               json=QUERY, headers=HEADERS, timeout=TIMOUT_TIME, proxies=proxy)
        dict_response = json.loads(answer.text)

        if dict_response.get("data").get("user") is None:
            return ()

        if dict_response['data']['user']['stream']:
            # Returns if the stream is live
            return streamer_name, dict_response['data']['user']['stream']['id']

    except requests.exceptions.RequestException or requests.exceptions.Timeout or Exception as e:
        if throw_error:
            raise RuntimeError(repr(e))
    return ()


def get_response(streamer_name: str, proxies: [str], throw_error=False):
    """
    If the broadcaster is in his own stream then he is live
    :param throw_error:
    :param proxies:
    :param streamer_name: Name of the stream to be checked
    :return: Returns the response if the stream is live, else returns None
    """
    # Doesnt work if not lower
    proxy = None
    if proxies is not None:
        proxy_choice = random.choice(proxies)
        proxy = {"http://": proxy_choice, "https://": proxy_choice}

    try:
        streamer_name = streamer_name.lower()
        response = json.loads(requests.get("http://tmi.twitch.tv/group/user/%s/chatters" % streamer_name,
                                           timeout=TIMOUT_TIME, proxies=proxy).text)
        return response
    except requests.HTTPError or requests.ConnectionError or Exception as e:
        if throw_error:
            raise RuntimeError(repr(e))
    return ()


def get_proxies():
    try:
        """
        # https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/
        :return: Returns a list of free proxies to use
        """
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxy_list = []
        for i in parser.xpath('//tbody/tr')[:10]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxy_list.append(proxy)
        return proxy_list
    except Exception as e:
        print(repr(e))
        return []


def get_live_streamer_list(streamer_list: [str]) -> [str]:
    proxies = get_proxies()
    live_list = {}
    with tqdm(total=len(streamer_list)) as pbar:
        pbar.set_description("Fetching current live")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(is_live, streamer, proxies): streamer for streamer in streamer_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pbar.update(1)
                try:
                    if future.result():
                        live_list[future.result()[0]] = future.result()[1]
                finally:
                    pass
    return live_list


def get_response_from_streamer_list(*, streamer_list: [str]) -> dict:
    proxies = get_proxies()
    live_dict = {}
    with tqdm(total=len(streamer_list)) as pbar:
        pbar.set_description("Fetching Steamer-data")
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {executor.submit(get_response, streamer, proxies): streamer for streamer in streamer_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pbar.update(1)
                streamer = future_to_url[future]
                try:
                    if future.result():
                        live_dict[streamer] = get_viewers(future.result())
                finally:
                    pass
                    # Log later
    return live_dict


if __name__ == "__main__":
    pass
