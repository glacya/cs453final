def add_elements(arr, k):
    return sum(x for x in arr[:k] if 9 < x < 100)