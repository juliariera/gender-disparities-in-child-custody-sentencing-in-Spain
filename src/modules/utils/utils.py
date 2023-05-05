
def flatten_list_of_lists(list_of_lists):
    _list = [item for sublist in list_of_lists for item in sublist]
    return _list