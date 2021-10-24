import time

from file_management import get_x_as_set, get_existing_as_sets
from viewer_handling.clustering.clustering import generate_clusters, cluster_fast
from viewer_handling.generate_current_snapshot import generate_network


def render():
    from settings import Set_Size, Streamer_List
    streamer_list = open(Streamer_List, "r").read().splitlines()
    streamer_dict = get_existing_as_sets(streamer_list, Set_Size)

    network = generate_network(streamer_dict)
    clusters = generate_clusters(edges=network.get("edges"), nodes=network.get("nodes"))

    cluster_list2 = cluster_fast(clusters, cluster_zip=2, iter_count=True)
    for cluster in cluster_list2:
        print(cluster)

    # Store edges and nodes as well as the groups together
    return


if __name__ == "__main__":
    render()
