import concurrent.futures
import concurrent.futures.thread
import json
import requests
from tqdm import tqdm
from viewer_handling.get_viewers import get_viewers


def get_response(streamer_name: str) -> dict:
    """
    If the broadcaster is in his own stream then he is live
    :param streamer_name: Name of the stream to be checked
    :return: Returns the response if the stream is live, else returns None
    """
    # Doesnt work if not lower
    try:
        streamer_name = streamer_name.lower()
        response = json.loads(requests.get("http://tmi.twitch.tv/group/user/%s/chatters" % streamer_name).text)
        contents = requests.get('https://www.twitch.tv/' + streamer_name).content.decode('utf-8')

        if 'isLiveBroadcast' in contents:
            return response
    except requests.HTTPError or requests.ConnectionError or Exception:
        pass
    return {}


def get_response_from_streamer_list(*, streamer_list: [str]) -> [tuple]:
    live_dict = {}
    with tqdm(total=len(streamer_list)) as pbar:
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            future_to_url = {executor.submit(get_response, streamer): streamer for streamer in streamer_list}
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
