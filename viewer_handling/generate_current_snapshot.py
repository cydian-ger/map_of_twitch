import csv
from datetime import datetime

from tqdm import tqdm

from viewer_handling.get_overlap import get_overlap


# Overlap percentage is important for clustering
OVERLAP_PERCENTAGE = 0.001


def generate_current_snapshot(overlap_dict: dict, **kwargs) -> dict:
    edges = []
    nodes = []
    name = str(datetime.now().strftime("result/%y_%m_%d_%H_%M_%S"))
    with open(name + "_edges.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        # Writes header
        writer.writerow(["Source", "Target", "Weight"])
        # From here the other streamers are removed
        overlap_list = list(overlap_dict.keys())

        for streamer in overlap_list:
            count = 0

            for streamer_2 in overlap_list:

                # If the streamer is not himself check for overlap
                if streamer_2 != streamer:

                    # Writes current node in
                    overlap = get_overlap(overlap_dict[streamer], overlap_dict[streamer_2])
                    if overlap > 0:

                        # Increases count of connections by 1
                        count += 1

                        writer.writerow((streamer, streamer_2, overlap))
                        edges.append((streamer, streamer_2, overlap))

            # If a streamer has no connections it builds one to himself
            # With the count variable
            # If someone is the last one scanned they are connected to themselves
            if count == 0:
                writer.writerow([streamer, streamer, 0])
                edges.append((streamer, streamer, 0))

            # Removes streamer from the dict as to not have doubles
            overlap_list.remove(streamer)

    with open(name + "_nodes.csv", "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Source", "Weight"])
        overlap_list = list(overlap_dict.keys())

        for streamer in overlap_list:
            length = len(overlap_dict[streamer]) * OVERLAP_PERCENTAGE
            writer.writerow((streamer, length))
            nodes.append((streamer, length))
    return {"name": name, "edges": edges, "nodes": nodes}


def generate_network(overlap_dict: dict, **kwargs) -> dict:
    """
    USE THIS THING
    np.intersect1d(arr1, arr2, assume_unique=True)

    :param overlap_dict:
    :param kwargs:
    :return:
    """

    edges = []
    nodes = []
    overlap_list = list(overlap_dict.keys())

    drop_single = False
    if kwargs.__contains__("drop_single") and kwargs.get("drop_single"):
        drop_single = True
    drop_list = []

    with tqdm(total=round(len(overlap_list) / 2) + 1) as pbar:
        pbar.set_description("Generating a Network ")
        for streamer in overlap_list:
            count = 0
            for streamer_2 in overlap_list:
                if streamer_2 != streamer:
                    overlap = get_overlap(overlap_dict[streamer], overlap_dict[streamer_2])
                    if overlap > 0:
                        count += 1
                        edges.append((streamer, streamer_2, overlap))

            if count == 0:
                if drop_single:
                    drop_list.append(streamer)
                else:
                    edges.append((streamer, streamer, 0))

            overlap_list.remove(streamer)
            pbar.update(1)

    overlap_list = list(overlap_dict.keys())

    if drop_single:
        for drop_streamer in drop_list:
            overlap_list.remove(drop_streamer)

    # Separate the single nodes / exclude them

    for streamer in overlap_list:
        length = len(overlap_dict[streamer]) * OVERLAP_PERCENTAGE
        nodes.append((streamer, length))

    return {"edges": edges, "nodes": nodes}


if __name__ == "__main__":
    generate_current_snapshot({})
