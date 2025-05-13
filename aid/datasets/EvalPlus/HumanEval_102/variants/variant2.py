def choose_num(x, y):
    """This function takes two positive numbers x and y and returns the
    biggest even integer number that is in the range [x, y] inclusive. If 
    there's no such number, then the function should return -1.
    For example:
    choose_num(12, 15) = 14
    choose_num(13, 12) = -1
    """
    
    even = False
    
    if x % 2 == 0 and y % 2 == 0:
        even = True
    
    while x <= y:
        if even:
            if y % 2 == 0:  # Check if y is even instead of x
                return y     # Return y instead of x
            else:
                y -= 1
        else:
            if x % 2 == 0:  # Check if x is even instead of y
                return x     # Return x instead of y
            else:
                x += 1
    
    return -1