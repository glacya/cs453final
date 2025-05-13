def strange_sort_list(lst):
    result = []
    lst.sort()
    i = 0
    j = len(lst) - 1
    while i <= j:
        if i == j:
            result.append(lst[i])
            break
        result.append(lst[i])
        result.append(lst[j])
        i += 1
        j -= 1
    return result