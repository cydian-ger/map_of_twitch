def serialize_sets(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj


def get_viewers(request) -> set:
    return set(request.get("chatters").get("viewers") + request.get("chatters").get("moderators")
               + request.get("chatters").get("vips") + request.get("chatters").get("broadcaster"))


def get_viewers_delta(request, old: set) -> set:
    new = set(request.get("chatters").get("viewers") + request.get("chatters").get("moderators")
               + request.get("chatters").get("vips"))
    return set.symmetric_difference(new, old)


if __name__ == "__main__":
    pass
    # json_str = json.dumps(set(), default=serialize_sets)
    # https://stackoverflow.com/questions/22736641/xor-on-two-lists-in-python
