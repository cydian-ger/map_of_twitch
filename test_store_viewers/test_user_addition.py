from viewer_handling.viewer_set import *


if __name__ == "__main__":
    # time1 = open("test.txt", "r").readlines()
    # time2 = open("test_addition.txt", "r").readlines()
    # union = set.union(set(time1), set(time2))
    # print(union)
    time1 = {"user1", "user2", "user3"}
    time2 = {"user1", "user4"}
    time3 = {"user1", "user3", "user5"}
    time4 = {"user6"}
    list_set = [time1, time2, time3, time4]
    """
    base_viewers = set(time1) - set()
    new_viewers = set(time2) - set(time1)
    left_viewers = set(time1) - set(time2)
    print(set.union(new_viewers, left_viewers))
    viewers = list_set[0]

    for _ in range(0, len(list_set) - 1):
        viewers = set.symmetric_difference(viewers, list_set[_ + 1])
    print(sorted(viewers, key=str.lower))
    """
    print(current_viewers_from_deltas(list_set))
    print(get_all_viewers_from_stream(list_set))
    # https://blog.finxter.com/union-multiple-sets-in-python/ add multiple sets
