def decimal_to_binary(decimal):
    if decimal >= 0 and decimal <= 255:
        binary = bin(decimal)[2:]
        return "db"+binary+"db"
    raise ValueError("The number must be in the range [0, 255]")