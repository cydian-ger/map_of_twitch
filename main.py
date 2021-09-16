from file_management import update_all_dirs, close_list
from file_management import update_all_dirs
from file_management import write
from viewer_handling.get_response import get_response_from_streamer_list, isLive


def get_new():
    """
    Checks all streamers and writes for all streamers that are online
    :return:
    """
    update_all_dirs(open("streamer_list", "r").read().splitlines())
    a = get_response_from_streamer_list(streamer_list=open("streamer_list", "r").read().splitlines(), include_not_live=True)
    for _ in list(a.keys()):
        if a[_] == {}:
            close_list(_)
        else:
            write(_, a[_])


if __name__ == '__main__':
    """
    schedule.every(15).minutes.do(get_new)
    get_new()
    while True:
        # Problem:
        # Checks for all scheduled tasks
        schedule.run_pending()
        time.sleep(0.1)
    """
    isLive("Tubbo")
    isLive("Tubbo")
