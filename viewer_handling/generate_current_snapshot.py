import csv
from datetime import datetime
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
                edges.append((streamer, streamer_2, 0))

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


if __name__ == "__main__":
    generate_current_snapshot({})
