import time
import schedule
from file_management import update_all_dirs
from file_management import write
from viewer_handling.get_response import get_response_from_streamer_list, get_response


def get_new():
    """
    Checks all streamers and writes for all streamers that are online
    :return:
    """
    update_all_dirs(open("streamer_list", "r").read().splitlines())
    a = get_response_from_streamer_list(streamer_list=open("streamer_list", "r").read().splitlines())
    for _ in list(a.keys()):
        write(_, a[_][0], a[_][1])


if __name__ == '__main__':
    schedule.every(15).minutes.do(get_new)
    get_new()
    while True:
        # Problem:
        # Checks for all scheduled tasks
        schedule.run_pending()
        time.sleep(0.1)
