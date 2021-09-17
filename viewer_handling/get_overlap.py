def get_overlap_percentage(length1: int, length2: int):
    return round(((length1 + length2) / 2) * 0.0175)
# What is the overlap percentage
# ((len(dict) + len(dict)) / 2) * 0.01%


def get_overlap(set1: set, set2: set):
    a = len(set1.intersection(set2))
    # if a <= get_overlap_percentage(len(set1), len(set2)):
    if a <= 300:
        return 0
    return len(set1.intersection(set2))


if __name__ == "__main__":
    # L
    pass
