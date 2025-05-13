def pluck(arr):
    if len(arr) == 0:
        return []
    even_values = [(value, index) for index, value in enumerate(arr) if value % 2 == 0]
    
    if len(even_values) == 0:
        return []
    
    min_even_value = min(even_values)
    return [min_even_value[0], min_even_value[1]]