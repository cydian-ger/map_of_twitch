import csv
from datetime import datetime
from os import listdir, rename
from pathlib import Path

viewer_dir = "viewer_sets"
file_ending = ".txt"


def update_all_dirs(streamer_list: list):
    for streamer in streamer_list:
        Path(viewer_dir + "/" + streamer.lower()).mkdir(parents=True, exist_ok=True)


def read(path: str) -> [str]:
    """
    Wow
    :param path:
    :return:
    """
    with open(path, "r", newline='') as csv_file:
        reader = csv.reader(csv_file)
        # Reads the line
        # Note that the docs are only 1 line long
        return next(reader)


def write(streamer: str, viewers: [str], stream_id: str):
    """
    Writes to a list, creates a new one if no old one exists
    :param viewers:
    :param streamer:
    :param stream_id:
    :return:
    """
    path = viewer_dir + "/" + streamer
    path_file = viewer_dir + "/" + streamer + "/" + stream_id
    files = sorted(listdir(path), reverse=True)
    # If a stream viewer count for this specific stream exists, write it into the old file
    # By loading the old viewers and set.unioning (aka unique merging) them together and
    # Over-writing the olds files content.
    if files.__contains__(stream_id):
        old_viewers = read(path_file)
        # New viewers is a set of old viewers + new viewers, as to guarantee uniqueness
        viewers = sorted(list(set(old_viewers).union(viewers)))

    with open(path_file, "w", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(viewers)
        csv_file.close()
        return


def get_all_as_set(streamer: str) -> set:
    """
    Returns all files from a streamers directory
    :param streamer:
    :return:
    """
    path = viewer_dir + "/" + streamer
    files = sorted(listdir(path), reverse=True)

    if len(files) == 0:
        return set()

    viewers = []
    for file in files:
        viewers += read(path + "/" + file)

    return set(viewers)


def get_x_as_set(streamer: str, amount: int, args=None, **kwargs) -> set:
    """
    Returns the last x amount of files in a dir as a viewer_set

    KWARGS: exclude_low: excludes all results below x, default = 0
    :param amount:
    :param streamer:
    :param args:
    :param kwargs:
    :return:
    """
    path = viewer_dir + "/" + streamer
    files = sorted(listdir(path), reverse=True)

    if len(files) == 0:
        return set()

    if kwargs.__contains__("exclude_low") and len(files) < kwargs.get("exclude_low"):
        return set()

    viewers = []

    # If the amount required is more than there are files
    # But also low files are not excluded: change the amount to len of files
    if amount > len(files):
        amount = len(files)

    for _ in range(0, amount):
        viewers = viewers + read(path + "/" + files[_])

    return set(viewers)
