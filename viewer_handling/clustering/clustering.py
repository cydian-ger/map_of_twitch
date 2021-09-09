# https://reader.elsevier.com/reader/sd/pii/S1877050914004256?token=24DC1F6D4C76BD0565A3D04DEBCC9BFFEA1915474CDB5697DD8112A6857484448E7DC20658C0AFB14DE8A792BC3F143E&originRegion=eu-west-1&originCreation=20210907025251
# This algorithm is entirely based on the paper listed above
from tqdm import tqdm
from viewer_handling.clustering.cluster import Cluster
from viewer_handling.clustering.cluster_function import create_attractiveness_list, can_merge
import warnings


def generate_clusters(*, edges: list, nodes: list, **kwargs) -> [Cluster]:
    """
    :param edges: list of edges, one edge = (source, target, weight)
    :param nodes: list of nodes (source, weight)
    :param kwargs:

        edges have to be unique,
        nodes have to be unique,
    :return returns cluster list:
    """
    if not nodes or not edges:
        raise ValueError("Node_list or edge_list empty, computation not possible")

    cluster_list = []
    for node in nodes:
        node_edge_list = []
        for edge in edges:
            if node[0] == edge[0] or node[0] == edge[1]:
                node_edge_list.append(edge)
        cluster_list.append(Cluster(node_edge_list, [node]))
    return cluster_list


def __cluster_return(cluster_list: list[Cluster], args) -> list[Cluster]:
    # This method manipulates the resulting cluster_list before return

    # no docstring needed all is explained in cluster()
    if args.__contains__("cluster_zip"):
        solo_cluster_list = []
        multi_cluster_list = []

        # divides cluster by the amount of nodes
        for cluster in cluster_list:
            if len(cluster.node_list) > args.get("cluster_zip"):
                multi_cluster_list.append(cluster)
            else:
                solo_cluster_list.append(cluster)

        # if there are no or a single solo clusters don't zip them
        if len(solo_cluster_list) <= 1:
            return cluster_list

        solo_cluster = solo_cluster_list[0]
        for cluster in solo_cluster_list:
            # Creates a big cluster from the small ones
            if cluster != solo_cluster:
                solo_cluster.merge(cluster)

        # Adds the solo cluster amalgamation to the end of multi_cluster list
        multi_cluster_list.append(solo_cluster)

        # It can continue after this routine
        cluster_list = multi_cluster_list

    if args.__contains__("cluster_omit_below_x") and args.get("cluster_omit_below_x"):
        new_cluster_list = []

        for cluster in cluster_list:
            if len(cluster.node_list) > args.get("cluster_omit_below_x"):
                new_cluster_list.append(cluster)

        # The program can continue after this routine
        cluster_list = new_cluster_list

    if args.__contains__("cluster_ignore_islands") and args.get("cluster_ignore_islands"):
        new_cluster_list = []
        # This ignores any clusters not connected to any other clusters
        for cluster in cluster_list:
            if not not cluster.edge_list:
                new_cluster_list.append(cluster)
        cluster_list = new_cluster_list

    if args.__contains__("cluster_amount"):
        if args.get("cluster_amount") < len(cluster_list):
            warnings.warn("Could not reach cluster amount %s. Bigger / less clusters are likely not possible "
                          % args.get("cluster_amount"), RuntimeWarning)
    return cluster_list


def cluster(cluster_list: list[Cluster], **kwargs) -> list[Cluster]:
    """
    This method divides a list of clusters into adequate clusters

    PARAM:

    cluster_list: List of cluster objects

    KWARGS:

    "iter_max" -> int: max amount of iterations before it returns, default = 10000

    "iter_max_auto" -> bool: if True overwrites iter_max with a calculated optimum, default = True

    "iter_count" -> bool: if True enables tqdm progress bar

    "iter_cluster_max" -> int: stops if the amount of clusters == this value, default = -1

    "cluster_zip" -> bool: all single clusters are zipped into a group, the last cluster in the list,
    default = -1

    "cluster_omit_below_x" -> int: all clusters with less nodes than x are ignored and thrown away, default = -1

    "cluster_ignore_islands" -> bool: if a cluster has no outward edges, aka is only connected to itself, ignore it,
    default = False

    :returns Returns a list of Cluster objects, that were merged by the clustering algorithm:
    """

    # Given the assumption that a merge happens ever iteration
    # The amount of iterations should be n - 2, since it breaks last iter and it need 1 empty run
    iter_max = len(cluster_list) - 2
    if kwargs.__contains__("iter_max_auto") or kwargs.__contains__("iter_max"):
        if not kwargs.get("iter_max_auto"):
            iter_max = 10000
            if kwargs.__contains__("iter_max"):
                iter_max = kwargs.get("iter_max")
                if iter_max < 0:
                    raise IndexError

    iter_count = True
    if kwargs.__contains__("iter_count"):
        iter_count = not (kwargs.get("iter_count"))

    iter_cluster_max = -1
    if kwargs.__contains__("iter_cluster_max"):
        iter_cluster_max = kwargs.get("iter_cluster_max")

    clustered_list = cluster_list

    progress = tqdm(range(0, iter_max), disable=iter_count)
    for _ in progress:
        # Keeps track of if
        changed = False
        attractiveness_list = create_attractiveness_list(clustered_list)
        for attr in attractiveness_list:
            # Checks if merge is possible

            if can_merge(clustered_list[attr[1]], clustered_list[attr[2]], attr[0]):
                # Merges the two clusters
                clustered_list[attr[1]].merge(cluster_list[attr[2]])
                # Removes the now merged second cluster
                clustered_list.pop(attr[2])
                # indicates that a merge has happened
                changed = True
                break

        # Returns if the desired amount of clusters is reached KWARGS
        if len(clustered_list) == iter_cluster_max:
            return __cluster_return(cluster_list, kwargs)

        # If no change or merge has happened this iteration, return
        if not changed:
            return __cluster_return(cluster_list, kwargs)

    return __cluster_return(cluster_list, kwargs)
