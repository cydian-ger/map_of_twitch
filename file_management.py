import csv
from datetime import datetime
from os import listdir, rename
from pathlib import Path

viewer_dir = "viewer_sets"
file_ending = ".txt"


def update_all_dirs(streamer_list: list):
    for streamer in streamer_list:
        Path(viewer_dir + "/" + streamer.lower()).mkdir(parents=True, exist_ok=True)


def has_open_list(streamer: str) -> str:
    """

    :param streamer:
    :return:
    """
    path = viewer_dir + "/" + streamer
    files = sorted(listdir(path), reverse=True)

    # If no entry exists return None
    if len(files) == 0:
        return ""

    if not files[0].endswith(file_ending):
        # If the latest file is not finished
        return path + "/" + files[0]
    else:
        return ""


def new_list_name(streamer: str) -> str:
    """
    IMPORTANT! -> check if open list exists before creating new one
    :param streamer:
    :return:
    """
    path = viewer_dir + "/" + streamer + "/"
    name = path + str(datetime.now().strftime("%y_%m_%d_%H_%M_%S"))
    return name


def read(path: str) -> [str]:
    """
    Wow
    :param path:
    :return:
    """
    with open(path, "r", newline='') as csv_file:
        reader = csv.reader(csv_file)
        # Needs the line
        return next(reader)


def write(streamer: str, viewers: [str]):
    """
    Writes to a list, creates a new one if no old one exists
    :param viewers:
    :param streamer:
    :return:
    """
    open_list = has_open_list(streamer)
    if open_list == "":
        with open(new_list_name(streamer), "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(viewers)
            csv_file.close()
            return
    else:
        old_viewers = read(open_list)
        # New viewers is a set of old viewers + new viewers, as to guarantee uniqueness
        new_viewers = sorted(list(set(old_viewers).union(viewers)))

        with open(open_list, "w", newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(new_viewers)
            csv_file.close()
    return


def close_list(streamer):
    path = viewer_dir + "/" + streamer
    files = sorted(listdir(path), reverse=True)

    if len(files) == 0:
        return

    for file in files:
        if not file.endswith(file_ending):
            rename(path + "/" + file, path + "/" + file + file_ending)


def get_all_set(streamer):
    """
    Returns all files from a streamers directory
    :param streamer:
    :return:
    """
    return


def get_x_set(streamer: str, amount: int, **kwargs):
    """
    Returns the last x amount of files in a dir as a viewer_set

    KWARGS: exclude_low: excludes all results below x
    :param amount:
    :param streamer:
    :param kwargs:
    :return:
    """
    path = viewer_dir + "/" + streamer
    files = sorted(listdir(path), reverse=True)

    old_viewers = []
    viewers = []
    viewers = sorted(list(set(old_viewers).union(viewers)))
    if kwargs.__contains__("exclude_low") and kwargs.get("exclude_low") is True:
        return {}
