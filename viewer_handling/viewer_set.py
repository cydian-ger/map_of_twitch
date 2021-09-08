def current_viewers_from_deltas(set_list: [set]) -> set:
    # XOR s the current list of viewers with the previous one,
    # If a user is in the list and appears in the next one that means they left
    # IF they arent in the current one but appear in the next one that means that they just tuned in
    viewers = set_list[0]
    for _ in range(0, len(set_list) - 1):
        viewers = set.symmetric_difference(viewers, set_list[_ + 1])
    return set(viewers)


def get_all_viewers_from_stream(set_list: [set]) -> set:
    # unions all viewers from a stream, so that each viewer is present in the list once
    return set.union(*set_list)
