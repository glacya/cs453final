def strange_sort_list(lst):
    result = []
    lst_copy = lst.copy()
    while lst_copy:
        result.append(min(lst_copy))
        lst_copy.remove(min(lst_copy))
        
        if lst_copy:
            result.append(max(lst_copy))
            lst_copy.remove(max(lst_copy))
    return result