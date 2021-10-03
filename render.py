# https://www.machinelearningplus.com/python/cprofile-how-to-profile-your-python-code/
import cProfile
import pstats
from file_management import get_existing_as_sets
from viewer_handling.clustering.clustering import generate_clusters, cluster_main
from viewer_handling.generate_current_snapshot import generate_network


def render():
    from settings import Set_Size, Streamer_List
    streamer_list = open(Streamer_List, "r").read().splitlines()
    streamer_dict = get_existing_as_sets(streamer_list, Set_Size)

    network = generate_network(streamer_dict, drop_single=True)

    clusters = generate_clusters(edges=network.get("edges"), nodes=network.get("nodes"))

    cluster_list2 = cluster_main(clusters, cluster_zip=2, iter_count=True)
    for cluster in cluster_list2:
        print(cluster)

    # Store edges and nodes as well as the groups together
    return


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    render()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('tottime')
    stats.print_stats()

"""
  n-calls   tottime  percall  cumtime  percall filename:lineno(function)
  1012389   56.566    0.000   56.566    0.000 {method 'intersection' of 'set' objects}
 22523800   18.667    0.000   18.667    0.000 E:\Projects\map_of_twitch\viewer_handling\clustering\cluster_function.py:5(get_overlap_edges_sum)
 22523800   11.863    0.000   36.129    0.000 E:\Projects\map_of_twitch\viewer_handling\clustering\cluster_function.py:46(return_attractiveness)
       37    6.304    0.170   42.469    1.148 E:\Projects\map_of_twitch\viewer_handling\clustering\cluster_function.py:78(create_highest_attractiveness_pairs)
 22524383    3.258    0.000    3.258    0.000 E:\Projects\map_of_twitch\viewer_handling\clustering\cluster.py:78(__eq__)
     1750    2.684    0.002    2.684    0.002 {method 'acquire' of '_thread.lock' objects}
46067545/46067389    2.409    0.000    2.409    0.000 {built-in method builtins.len}
        1    0.847    0.847   58.083   58.083 E:\Projects\map_of_twitch\viewer_handling\generate_current_snapshot.py:64(generate_network)
  1009830    0.500    0.000   57.134    0.000 E:\Projects\map_of_twitch\viewer_handling\get_overlap.py:7(get_overlap)
"""
