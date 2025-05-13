def sum_squares(lst):
    # empty list
    if len(lst) == 0:
        return 0
    # list with one element
    if len(lst) == 1:
        return lst[0]
    # list with two elements
    if len(lst) == 2:
        return lst[0] + lst[1]
    # list with more than two elements
    else:
        lst_len = len(lst)
        updated_lst = []
        for i in range(lst_len):
            if (i % 3 == 0):
                updated_lst.append(lst[i]**2)
            elif (i % 4 == 0) and (i % 3 != 0):
                updated_lst.append(lst[i]**3)
            else:
                updated_lst.append(lst[i])
        return sum(updated_lst)