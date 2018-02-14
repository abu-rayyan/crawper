
MESSAGES = {
    "Test": "Hello World"
}


def find_item(obj, key):
    """
    To find an item in a dictionary object, may become handy in future
    :param obj: dict object
    :param key: key to find
    :return: returns item
    """
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = find_item(v, key)
            if item is not None:
                return item
