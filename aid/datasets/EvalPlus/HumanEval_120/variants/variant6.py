def maximum(arr, k):
    if k == 0: 
        return []
    if k == 1: 
        return [max(arr)]
    if k == len(arr): 
        return sorted(arr)
    # sort the array
    arr.sort(reverse=True)
    # Find the k largest elements
    return arr[:k]