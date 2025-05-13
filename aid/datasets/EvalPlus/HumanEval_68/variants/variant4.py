def pluck(arr):
    if len(arr) == 0:
        return []
    min_even_value = float('inf')
    min_even_index = float('inf')
    
    for index, item in enumerate(arr):
        if item % 2 == 0 and item < min_even_value:
            min_even_value = item
            min_even_index = index
            
    if min_even_value == float('inf'):
        return []
    
    return [min_even_value, min_even_index]