# Test check if time is better with dict than it is with list
# First generate random text
import csv
import json
from viewer_handling.clustering.clustering import generate_clusters
from viewer_handling.clustering.clustering import cluster
from viewer_handling.generate_current_snapshot import generate_current_snapshot
from viewer_handling.get_response import get_response_from_streamer_list

if __name__ == "__main__":
    # https://stackoverflow.com/questions/12064130/is-there-any-way-to-check-if-a-twitch-stream-is-live-using-python
    # a = get_response_from_streamer_list(streamer_list=open("streamer_list", "r").read().splitlines())
    # b = generate_current_snapshot(a)
    # # generate(b.get("name"), a)
    # csv_name = "result/21_09_08_04_38_48"
    csv_name = "result/21_09_08_19_37_11"
    #

    with open(csv_name + "_edges.csv", newline='') as f:
        reader = csv.reader(f)
        # Skips the headers
        next(reader)
        edges = []
        for row in reader:
            edges.append((row[0], row[1], float(row[2])))

    with open(csv_name + "_nodes.csv", newline='') as f:
        reader = csv.reader(f)
        next(reader)
        nodes = []
        for row in reader:
            nodes.append((row[0], float(row[1])))

    clusters = cluster(cluster_list=generate_clusters(edges=edges, nodes=nodes), cluster_omit_below_x=2, iter_count=True, cluster_zip=2)

    json_dict = {}
    # Makes it ready for json
    node_dict_list = []
    for _ in range(0, len(clusters)):
        for node in clusters[_].get_nodes():
            # Write it as string so that the indent is not way to big and the file then is too, in line numbers
            node_dict_list.append({"id": node, "group": _ + 1})

    json_dict.update({"nodes": node_dict_list})

    # Makes it ready for json
    edge_dict_list = []
    for edge in edges:
        edge_dict_list.append({"source": edge[0], "target": edge[1], "value": edge[2]})

    for clust in clusters:
        print(clust)

    json_dict.update({"links": edge_dict_list})

    # PROBLEM -> STRINGS ARE STORED AS STRING AND NOT AS IS
    open("json_dict.json", "w").write(json.dumps(json_dict, indent=4))
