
def sort_array(array):


    if array == []: return []
    return sorted(array, reverse=(array[0]+array[-1]) % 2 == 0)

