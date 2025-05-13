def smallest_change(arr):
    if not arr:
        return 0
    num_changes = 0
    for i in range(len(arr) // 2):
        if arr[i] != arr[len(arr) - 1 - i]:
            num_changes += 1
    return num_changes