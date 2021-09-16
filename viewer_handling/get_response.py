import concurrent.futures
import concurrent.futures.thread
import json
import requests
from tqdm import tqdm
from viewer_handling.get_viewers import get_viewers


def isLive(username):
    """
    https://stackoverflow.com/questions/12064130/is-there-any-way-to-check-if-a-twitch-stream-is-live-using-python
    NOTE BIG NOTE -> THIS METHOD RETURNS THE STREAM ID SO I CAN SAVE STREAMS BY ID INSTEAD OF TIME STAMPS, THIS IS HUGE
    :param username:
    :return:
    """
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

    QUERY = {
        'query': GQL_QUERY,
        'variables': {
            'login': username
        }
    }

    response = requests.post('https://gql.twitch.tv/gql',
                             json=QUERY, headers=HEADERS)
    dict_response = response.json()
    # Returns stream id if live, else returns nothing
    return dict_response['data']['user']['stream'] if dict_response['data']['user']['stream'] is not None else None


def get_response(streamer_name: str) -> tuple:
    """
    If the broadcaster is in his own stream then he is live
    :param streamer_name: Name of the stream to be checked
    :return: Returns the response if the stream is live, else returns None
    """
    # Doesnt work if not lower
    try:
        streamer_name = streamer_name.lower()
        response = json.loads(requests.get("http://tmi.twitch.tv/group/user/%s/chatters" % streamer_name).text)

        live = isLive(streamer_name)
        # If string not empty / None
        if not not live:
            return response, live
    except requests.HTTPError or requests.ConnectionError:
        pass
    return ()


def get_response_from_streamer_list(*, streamer_list: [str], include_not_live=False) -> dict:
    live_dict = {}
    with tqdm(total=len(streamer_list)) as pbar:
        pbar.set_description("Fetching Steamer-data")
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            future_to_url = {executor.submit(get_response, streamer): streamer for streamer in streamer_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pbar.update(1)
                streamer = future_to_url[future]
                try:
                    if future.result():
                        live_dict[streamer] = get_viewers(future.result())
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
