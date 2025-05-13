def prod_signs(arr):
    """
    You are given an array arr of integers and you need to return
    sum of magnitudes of integers multiplied by product of all signs
    of each number in the array, represented by 1, -1 or 0.
    Note: return None for empty arr.
    Example:
    >>> prod_signs([1, 2, 2, -4]) == -9
    >>> prod_signs([0, 1]) == 0
    >>> prod_signs([]) == None
    """
    if len(arr) == 0:
        return None
    else:
        signs = set()
        for x in arr:
            if x > 0:
                signs.add(1)
            elif x < 0:
                signs.add(-1)
            else:
                signs.add(0)
        if len(signs) == 1:
            sign = signs.pop()
            if sign == 0:
                return 0
            else:
                return sum(arr) * sign
        else:
            return sum([abs(x) for x in arr]) * 0