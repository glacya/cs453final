def closest_integer(value):
    if '.' in value:
        value = float(value)
        if value % 1 == 0.5:
            if value >= 0:
                return int(value + 0.5)
            else:
                return int(value - 0.5)
        else:
            return int(round(value))
    else:
        return int(value)