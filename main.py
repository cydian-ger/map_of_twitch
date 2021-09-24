import time
import schedule
from file_management import update_all_dirs
from file_management import write
from viewer_handling.get_response import get_response_from_streamer_list, get_live_streamer_list


def get_new():
    """
    Checks all streamers and writes for all streamers that are online
    :return:
    """
    update_all_dirs(open("streamer_list", "r").read().splitlines())
    live_streamers = get_live_streamer_list(streamer_list=open("streamer_list", "r").read().splitlines())
    streamers = get_response_from_streamer_list(streamer_list=list(live_streamers.keys()))
    for streamer in list(streamers.keys()):
        write(streamer, list(streamers[streamer]), live_streamers[streamer])


if __name__ == '__main__':
    schedule.every(15).minutes.do(get_new)
    get_new()
    while True:
        # Problem:
        # Checks for all scheduled tasks
        schedule.run_pending()
        time.sleep(0.1)
