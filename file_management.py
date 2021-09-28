import concurrent.futures
import concurrent.futures.thread
import csv
from os import listdir
from pathlib import Path

from tqdm import tqdm

viewer_dir = "viewer_sets"


def update_all_dirs(streamer_list: list):
    Path(viewer_dir).mkdir(parents=True, exist_ok=True)
    for streamer in streamer_list:
        Path(viewer_dir + "/" + streamer.lower()).mkdir(parents=True, exist_ok=True)


def read(path: str) -> [str]:
    """
    Wow such code
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

    # Returns empty set
    if len(viewers) == 0:
        return set()

    return set(viewers)


def get_existing_as_sets(streamer_list: [str], amount: int, args=None, **kwargs) -> [set]:
    """
    :param streamer_list:
    :param amount:
    :param args:
    :param kwargs:
    :return:
    """
    from settings import Max_Workers
    response_dict = {}

    with tqdm(total=len(streamer_list)) as pbar:
        pbar.set_description("Getting Viewer-sets  ")
        with concurrent.futures.ThreadPoolExecutor(max_workers=Max_Workers) as executor:
            future_to_url = {executor.submit(get_x_as_set, streamer, amount): streamer for streamer in streamer_list}
            for future in concurrent.futures.as_completed(future_to_url):
                pbar.update(1)
                streamer = future_to_url[future]
                try:
                    if future.result():
                        response_dict[streamer] = future.result()
                finally:
                    pass
                    # Log later
    return response_dict
