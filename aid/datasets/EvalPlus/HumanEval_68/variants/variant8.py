def pluck(arr):
    if len(arr) == 0:
        return []
    min_value = float('inf')
    min_index = None
    for index, item in enumerate(arr):
        if item % 2 == 0 and item < min_value:
            min_value = item
            min_index = index
    if min_index is not None:
        return [min_value, min_index]
    else:
        return []