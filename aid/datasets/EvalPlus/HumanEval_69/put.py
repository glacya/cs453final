
def search(lst):
    '''
    You are given a non-empty list of positive integers. Return the greatest integer that is greater than 
    zero, and has a frequency greater than or equal to the value of the integer itself. 
    The frequency of an integer is the number of times it appears in the list.
    If no such a value exist, return -1.
    Examples:
        search([4, 1, 2, 2, 3, 1]) == 2
        search([1, 2, 2, 3, 3, 3, 4, 4, 4]) == 3
        search([5, 5, 4, 4, 4]) == -1
    '''
    if lst == []:
        return -1
    lst.sort()
    freq = [0] * (max(lst) + 1)
    for x in lst:
        freq[x] += 1

    for i in range(len(freq)-1, -1, -1):
        if i == 0:
            continue
        if freq[i] >= i and freq[i] > freq[i-1]:
            return i
    return -1

    # Other soluton
    # if len(lst) == 0:
    #     return -1
    # d = dict()
    # for x in lst:
    #     d[x] = d.get(x, 0) + 1
    #     if d[x] >= x:
    #         return x
    # return -1
