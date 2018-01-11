from __future__ import print_function

MESSAGES = {
    "Test": "Hello World"
}


def find_item(obj, key):
    if key in obj:
        return obj[key]
    for k, v in obj.items():
        if isinstance(v, dict):
            item = find_item(v, key)
            if item is not None:
                return item
