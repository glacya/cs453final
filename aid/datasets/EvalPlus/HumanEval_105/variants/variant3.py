def by_length(arr):
    if not arr:
        return []
    arr = sorted(filter(lambda x: 1 <= x <= 9, arr)) 
    arr.reverse()
    res = []
    for num in arr:
        if num == 1:
            res.append("One")
        elif num == 2:
            res.append("Two")
        elif num == 3:
            res.append("Three")
        elif num == 4:
            res.append("Four")
        elif num == 5:
            res.append("Five")
        elif num == 6:
            res.append("Six")
        elif num == 7:
            res.append("Seven")
        elif num == 8:
            res.append("Eight")
        elif num == 9:
            res.append("Nine")
    return res