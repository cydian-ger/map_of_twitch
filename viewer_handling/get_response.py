import concurrent.futures
import concurrent.futures.thread
import json
import requests
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


def get_response(streamer_name: str):
    """
    If the broadcaster is in his own stream then he is live
    :param streamer_name: Name of the stream to be checked
    :return: Returns the response if the stream is live, else returns None
    """
    # Doesnt work if not lower
    try:
        streamer_name = streamer_name.lower()
        response = json.loads(requests.get("http://tmi.twitch.tv/group/user/%s/chatters" % streamer_name).text)

        QUERY = {
            'query': GQL_QUERY,
            'variables': {
                'login': streamer_name
            }
        }

        dict_response = json.loads(requests.post('https://gql.twitch.tv/gql',
                                     json=QUERY, headers=HEADERS).text)

        # Gods please have mercy
        # A problem arises when a user doesnt exists
        # For the sole reason that then the ['data']['user']['stream'] function fails without exception
        #
        if dict_response.get("data").get("user") is None:
            return ()

        if dict_response['data']['user']['stream']:
            return response, dict_response['data']['user']['stream']['id']

    except requests.HTTPError or requests.ConnectionError:
        pass
    return ()


def get_response_from_streamer_list(*, streamer_list: [str], include_not_live=False) -> dict:
    live_dict = {}
    with tqdm(total=len(streamer_list)) as pbar:
        pbar.set_description("Fetching Steamer-data")
        with concurrent.futures.ThreadPoolExecutor(max_workers=64) as executor:
            future_to_url = {executor.submit(get_response, streamer): streamer for streamer in streamer_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pbar.update(1)
                streamer = future_to_url[future]
                try:
                    if future.result():
                        live_dict[streamer] = get_viewers(future.result()[0]), future.result()[1]
                    # If it is enabled to include non live streams:
                    elif include_not_live:
                        live_dict[streamer] = {}
                finally:
                    pass
                    # Log later
    return live_dict


def test_case_response() -> bool:
    """
    If this method works then the requests features work as intended
    :return:
    """
    try:
        get_response("cydian_")
        return True
    except Exception:
        return False


if __name__ == "__main__":
    pass
