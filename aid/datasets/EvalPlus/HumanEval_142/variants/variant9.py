def sum_squares(lst):
    if len(lst) == 0:
        return 0
    sum_squares = 0
    for i in range(len(lst)):
        if i % 3 == 0:
            sum_squares += lst[i] ** 2
        elif i % 4 == 0 and i % 3 != 0:
            sum_squares += lst[i] ** 3
        else:
            sum_squares += lst[i]
    return sum_squares