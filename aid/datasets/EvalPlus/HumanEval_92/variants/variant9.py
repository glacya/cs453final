def any_int(x, y, z):
    # Check if all numbers are integers
    if all(isinstance(i, int) for i in [x, y, z]):
        # Check if one of the numbers is equal to the sum of the other two
        if x == y + z or y == x + z or z == x + y:
            return True
    return False