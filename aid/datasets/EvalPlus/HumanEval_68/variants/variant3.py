def pluck(arr):
    if len(arr) == 0:
        return []
    even_values = [node for node in arr if node % 2 == 0]
    
    if not even_values:
        return []
    min_even_value = min(even_values)
    min_even_index = arr.index(min_even_value)
    return [min_even_value, min_even_index]