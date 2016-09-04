from collections import namedtuple


def dict_to_dot_notation(dictionary):
    form_tuple = namedtuple('form', dictionary.keys())
    return form_tuple(**dictionary)
