# https://reader.elsevier.com/reader/sd/pii/S1877050914004256?token=24DC1F6D4C76BD0565A3D04DEBCC9BFFEA1915474CDB5697DD8112A6857484448E7DC20658C0AFB14DE8A792BC3F143E&originRegion=eu-west-1&originCreation=20210907025251
# This algorithm is entirely based on the paper listed above
from tqdm import tqdm
from viewer_handling.clustering.cluster import Cluster
from viewer_handling.clustering.cluster_function import create_attractiveness_list, can_merge, \
    create_highest_attractiveness_pairs
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


def __cluster_return(cluster_list: list[Cluster], args):
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


def cluster_default(cluster_list: list[Cluster], args=None, **kwargs) -> list[Cluster]:
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

    # Overwrites the keyword args if there are none and arguments are provided
    if not not args and not kwargs:
        kwargs = args

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
    progress.set_description("Normal-calc Clusters ")
    for _ in progress:
        # Keeps track of if
        changed = False
        attractiveness_list = create_attractiveness_list(clustered_list)
        for attr in attractiveness_list:
            # Checks if merge is possible

            if can_merge(clustered_list[attr[1]], clustered_list[attr[2]], attr[0]):
                # Merges the two clusters
                clustered_list[attr[1]].merge(clustered_list[attr[2]])
                # Removes the now merged second cluster
                clustered_list.pop(attr[2])
                # indicates that a merge has happened
                changed = True
                break

        # Returns if the desired amount of clusters is reached KWARGS
        if len(clustered_list) == iter_cluster_max:
            return clustered_list

        # If no change or merge has happened this iteration, return
        if not changed:
            return clustered_list

    return clustered_list


def __quick_merge_clusters(merge_list_list: [int], clustered_list: [Cluster]):
    # For each cluster, has a list of the
    # Create graphs, pointers is the in list.
    return


def cluster_fast(cluster_list: list[Cluster], args=None, **kwargs) -> list[Cluster]:
    """
    As it seems it works just as well as normal clustering however is way faster
    :param cluster_list:
    :param args:
    :param kwargs:
    :return:
    """
    if not not args and not kwargs:
        kwargs = args

    iter_max = len(cluster_list) - 1

    iter_count = True
    if kwargs.__contains__("iter_count"):
        iter_count = not (kwargs.get("iter_count"))

    clustered_list = cluster_list

    progress = tqdm(range(0, iter_max), disable=iter_count)
    progress.set_description("Fastcalcing Clusters ")

    for _ in progress:

        changed = False
        attractiveness_list = create_highest_attractiveness_pairs(clustered_list)
        if not not attractiveness_list:
            changed = True

        merged = []

        for pair in attractiveness_list:
            clustered_list[pair[0]].merge(clustered_list[pair[1]])
            merged.append(pair[1])

        for i in sorted(merged, reverse=True):
            del (clustered_list[i])

        if not changed:
            break

    return clustered_list


def cluster_separate(cluster_list: list[Cluster], **kwargs) -> list[list[Cluster]]:
    """
    This method divides a list of clusters into adequate clusters

    PARAM:

    cluster_list: List of cluster objects

    KWARGS:

    """

    clustered_list = []

    separate_clusters = []

    clustered_list = cluster_fast(cluster_list, kwargs)

    cluster_list = __cluster_return(clustered_list, kwargs)
    return cluster_list


def cluster(cluster_list: list[Cluster], cluster_merge="default", **kwargs):
    """
    This method quickly (yet sloppily) divides clusters

    PARAM:

    cluster_list, list of clusters

    "cluster_merge" -> str:
                        "merge_single"/"default": merges a single element at a time and re-calculates the connections
                        [1->2]

                        cluster_default()

                        "merge_pairs"/"fast"/"": takes more time but, does not resolve cluster conflicts
                        [1->2][2->1]...[n->m][m->n]

                        cluster_fast(), on average, takes less than half of default, however i cant assure the result,
                        to be as clean as default, besides that default allows for more custom, changes
    :return:
    """

    clustered_list = []

    arg = cluster_merge
    if arg == "merge_single" or arg == "slow" or arg == "default" or arg == "":
        clustered_list = cluster_default(cluster_list, kwargs)

    elif arg == "merge_pairs" or arg == "fast":
        clustered_list = cluster_fast(cluster_list, kwargs)

    cluster_list = __cluster_return(clustered_list, kwargs)
    return cluster_list
