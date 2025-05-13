
def move_one_ball(arr):

    
    sorted_arr = sorted(arr)
    if arr == sorted_arr: return True
    for i in range(1, len(arr)):
        if arr[i:] + arr[:i] == sorted_arr:
            return True
    return False

