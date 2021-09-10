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
        return "nodes: %s, density: %s" % (node_names, self.return_density())

    def __repr__(self):
        return str(self)

"""
FUNCTIONS
"""
