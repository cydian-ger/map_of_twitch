import numpy as np
from viewer_handling.clustering.cluster import Cluster


def get_overlap_edges_sum(cluster1: Cluster, cluster2: Cluster) -> float:
    """
    This method returns the sum of all edges shared by both clusters,
    which means every edge that connects cluster (self) and (other).
    :param cluster1: The first cluster
    :param cluster2: The second cluster
    :return:
    """
    edge_overlap_sum = 0.0
    for edge in cluster1.edge_list:
        for other_edge in cluster2.edge_list:
            # If both edges are alike, but mirrored, (aka 1<->2 == 2<->1),
            # meaning that this is an edge that connects the two clusters
            # Add it to the total pull
            # Or both edges are the exact same
            if (edge[0] == other_edge[1] and edge[1] == other_edge[0]) or edge == other_edge:
                # Adds the weight to the edge
                edge_overlap_sum += edge[2]
    return edge_overlap_sum


def get_overlap_edges_amount(cluster1: Cluster, cluster2: Cluster) -> int:
    """
    This method returns
    :param cluster1: The first cluster
    :param cluster2: The second cluster
    :return: Returns amount of edges
    """
    edge_overlap_amount = 0
    for edge in cluster1.edge_list:
        for other_edge in cluster2.edge_list:
            # If both edges are alike, but mirrored, (aka 1<->2 == 2<->1),
            # meaning that this is an edge that connects the two clusters
            # Add it to the total pull
            # Or both edges are the exact same
            if (edge[0] == other_edge[1] and edge[1] == other_edge[0]) or edge == other_edge:
                # Adds the weight to the edge
                edge_overlap_amount += 1
    return edge_overlap_amount


def return_attractiveness(cluster1: Cluster, cluster2: Cluster) -> float:
    """
    Attractiveness of 2 clusters is determined by dividing the combined weight of shared edges,
    (edges that connect this cluster to the other cluster), by the multiplied amount of both clusters nodes
    At least over 50% speed increase for caching 1:31
    :param cluster1: first cluster
    :param cluster2: second cluster
    :return: Returns number value of attractiveness of 2 clusters
    """
    if cluster1 == cluster2:
        return 0.0
    # Returns the (Edge Sum Weight) / (NodeAmountSELF * NodeAmountOTHER)
    return get_overlap_edges_sum(cluster1, cluster2) / (len(cluster1.node_list) * len(cluster2.node_list))


def create_attractiveness_list(cluster_list: [Cluster]):
    """
    Creates an attractiveness list of all clusters
    List is stored in a descending way highest->lowest
    :param cluster_list:
    :return:
    """
    k = len(cluster_list)
    attractiveness_list = []
    for i in range(0, k):
        for j in range(i, k):
            if i != j:
                # This method appends the attractiveness and the cluster index for both clusters
                attractiveness_list.append((return_attractiveness(cluster_list[i], cluster_list[j]), i, j))
    return sorted(attractiveness_list, key=lambda x: x[0], reverse=True)


def create_highest_attractiveness_pairs(cluster_list: [Cluster]) -> list:
    """
    Creates the pairs of highest attracted clusters
    Gets the pointer and attractiveness value for every cluster, aka the cluster it is most interest in merging with,
    If a cluster is mutual 1:(2, 50) <-> 2:(1, 50) it is added to the list
    :param cluster_list: list of clusters
    :return: List of tuples (self_index, pointer_on_list, attr_value)
    """
    k = len(cluster_list)
    attractiveness_list = np.zeros(k, dtype=tuple)
    cluster_list_np = np.asarray(cluster_list)
    pairs = []
    for i in range(0, k):
        highest_attr = 0
        pos = -1
        for j in range(0, k):
            if i != j:
                attr = return_attractiveness(cluster_list_np[i], cluster_list_np[j])
                if attr > highest_attr:
                    highest_attr = attr
                    pos = j
        attractiveness_list[i] = (i, pos, highest_attr)

    for attr in attractiveness_list:
        if attr[0] == attractiveness_list[attr[1]][1]:
            if can_merge(cluster_list_np[attr[0]], cluster_list_np[attr[1]], attr[2]):
                pair = (min(attr[0], attr[1]), max(attr[0], attr[1]))
                if not pairs.__contains__(pair):
                    pairs.append(pair)
    return pairs


def is_inter_interested(cluster1: Cluster, cluster2: Cluster) -> bool:
    """
    Checks if two clusters meet the condition of being inter_interested
    :param cluster1: the first cluster
    :param cluster2: the second cluster
    :return:
    """
    overlap = get_overlap_edges_amount(cluster1, cluster2)
    return overlap >= len(cluster1.node_list) and overlap >= len(cluster2.node_list)


def can_merge(cluster1: Cluster, cluster2: Cluster, attractiveness: float) -> bool:
    """
    Checks if clusters can be merged by checking if
    the attractiveness value is greater than the sum of both clusters density
    :param attractiveness: attractiveness of both parameters, set to -1 to calculate attractiveness in this function
    :param cluster1: the first cluster
    :param cluster2: the second cluster
    :return: Returns True if the clusters can be merged
    """
    return attractiveness >= (cluster1.return_density() + cluster2.return_density())
