import hashlib
from functools import cache

import numpy as np


class Cluster:
    def __init__(self, edges: list, nodes: list):
        """
        @param edges: list of edges [source, target, weight]
        @param nodes: list of nodes [source, weight]
        :return:
        """
        self.edge_list = edges
        self.node_list = nodes
        # Clean up all edges that are contained only inside the cluster
        # So that for attractiveness the search is done easier
        return

    def return_density(self) -> int:
        """
        Cluster density is the average of all the weights of nodes in the cluster.
        :return:
        """
        return sum(node[1] for node in self.node_list) / len(self.node_list)

    def return_members(self) -> [str]:
        """
        Returns a list of members
        :return:
        """
        member_list = []
        for member in self.node_list:
            member_list.append(member[0])
        return member_list

    def merge(self, other):
        """
        First this method adds every node of the other Cluster, then it adds ever edge from the other cluster
        Given that internal edges are worthless to us, we can kick them out to increase computing time.
        TESTED - works
        :param other: other cluster
        :return:
        """
        # Update node list
        for node in other.node_list:
            self.node_list.append(node)

        # Update edge list
        for edge in other.edge_list:
            self.edge_list.append(edge)

        # Get all node names in set for look up time
        node_names = set()
        for node in self.node_list:
            node_names.add(node[0])

        # This gets rid of all edges that point from 1 cluster-internal node to another cluster-internal node
        new_edge_list = []
        for edge in self.edge_list:
            if not (node_names.__contains__(edge[0]) and node_names.__contains__(edge[1])):
                new_edge_list.append(edge)

        self.edge_list = new_edge_list
        return

    def get_nodes(self):
        """
        Returns the clear names of all nodes in a cluster
        :return:
        """
        node_names = []
        for node in self.node_list:
            node_names.append(node[0])
        return node_names

    def __hash__(self):
        # https://stackoverflow.com/questions/2511058/persistent-hashing-of-strings-in-python
        return int(hashlib.md5(str(self.get_nodes()).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        """
        Returns true if they have the same node and edge list
        :param other: Other cluster
        :return:
        """
        return self.edge_list == other.edge_list and self.node_list == other.node_list

    def __str__(self):
        node_names = self.get_nodes()
        return "|nodes: %s, edges: %s, density: %s|" % (node_names, self.edge_list, self.return_density())

    def __repr__(self):
        return str(self)
"""
FUNCTIONS
"""


def get_overlap_edges(cluster1: Cluster, cluster2: Cluster) -> list:
    """
        This method returns all edges shared by both clusters,
        which means every edge that connects cluster (self) and (other).
        :param cluster1: The first cluster
        :param cluster2: The second cluster
        :return:
        """
    edge_overlap_list = []
    for edge in cluster1.edge_list:
        for other_edge in cluster2.edge_list:
            # If both edges are alike, but mirrored, (aka 1<->2 == 2<->1),
            # meaning that this is an edge that connects the two clusters
            # Add it to the total pull
            # Or both edges are the exact same
            if (edge[0] == other_edge[1] and edge[1] == other_edge[0]) or edge == other_edge:
                edge_overlap_list.append(edge)
    return edge_overlap_list


@cache
def return_attractiveness(cluster1: Cluster, cluster2: Cluster) -> float:
    """
    Attractiveness of 2 clusters is determined by dividing the combined weight of shared edges,
    (edges that connect this cluster to the other cluster), by the multiplied amount of both clusters nodes
    At least over 50% speed increase for caching
    :param cluster1: first cluster
    :param cluster2: second cluster
    :return: Returns number value of attractiveness of 2 clusters
    """
    if cluster1 == cluster2:
        return 0.0
    edge_overlap_list = get_overlap_edges(cluster1, cluster2)
    # Returns the (Edge Sum Weight) / (NodeAmountSELF * NodeAmountOTHER)
    return sum(edge[2] for edge in edge_overlap_list) / (len(cluster1.node_list) * len(cluster2.node_list))


def create_attractiveness_list(cluster_list: [Cluster]) -> list:
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

    # Sorts this list by values
    return sorted(attractiveness_list, key=lambda x: x[0], reverse=True)


@cache
def is_inter_interested(cluster1: Cluster, cluster2: Cluster) -> bool:
    """
    Checks if two clusters meet the condition of being inter_interested
    :param cluster1: the first cluster
    :param cluster2: the second cluster
    :return:
    """
    overlap = len(get_overlap_edges(cluster1, cluster2))
    return overlap >= len(cluster1.node_list) and overlap >= len(cluster2.node_list)


@cache
def can_merge(cluster1: Cluster, cluster2: Cluster, attractiveness: float) -> bool:
    """
    Checks if clusters can be merged by checking if
    the attractiveness value is greater than the sum of both clusters density
    :param attractiveness: attractiveness of both parameters, set to -1 to calculate attractiveness in this function
    :param cluster1: the first cluster
    :param cluster2: the second cluster
    :return: Returns True if the clusters can be merged
    """
    # If attractiveness has not been calculated yet, calculate it
    if attractiveness == -1:
        attractiveness = return_attractiveness(cluster1, cluster2)

    return attractiveness >= (cluster1.return_density() + cluster2.return_density())


def create_attractiveness_matrix(cluster_list: [Cluster]) -> np.ndarray:
    """
    Creates the attractiveness list for each cluster towards each other cluster
    :param cluster_list:
    :return:
    """
    k = len(cluster_list)

    matrix = np.zeros((k, k))
    # Loops through every list
    for i in range(0, k):
        for j in range(i, k):
            if i != j:
                # Since its a mirrored table, you can write [i][j] and [j][i] at the same time,
                # however just writing [i][j] is enough for the clustering process,
                # This also avoids having the same value twice, for every value
                attractiveness = return_attractiveness(cluster_list[i], cluster_list[j])
                matrix[i][j] = attractiveness
                matrix[j][i] = attractiveness
            else:
                # If it is the same cluster, attractiveness is 0, so we can just keep the 0, aka do nothing
                # It is like that even with the extended calc so we can just not do the calc
                pass
    return matrix
