def is_sorted(lst):
    if len(lst) == 1:
        return True
    for i in range(len(lst)-1):
        if lst[i] >= lst[i+1]:  # Modify condition to include equality for duplicate numbers
            return False
        if i+2 < len(lst) and lst[i] == lst[i+1] and lst[i] == lst[i+2]:  # Add check for more than 1 duplicate of the same number
            return False
    return True