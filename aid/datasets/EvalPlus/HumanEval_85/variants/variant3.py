def add(lst):
    """Given a non-empty list of integers lst. add the even elements that are at odd indices..
    Examples:
        add([4, 2, 6, 7]) ==> 2 
    """
    x = len(lst) - 1  # Start from the last odd index
    ans = 0
    while x >= 0:  # Modified condition to include the first odd index
        if lst[x] % 2 == 0:
            ans += lst[x]
        x -= 2  # Move to the previous odd index
    return ans