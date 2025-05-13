def max_element(l: list):
    """Return maximum element in the list.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """
    if not l:  # check if the list is empty
        return None  # return None if the list is empty
    max_val = l[0]  # initialize max_val with the first element of the list
    for i in l:
        if i > max_val:
            max_val = i
    return max_val