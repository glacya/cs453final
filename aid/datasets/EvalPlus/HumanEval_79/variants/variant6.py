def decimal_to_binary(decimal):
    if 0 <= decimal <= 255:
        binary = bin(decimal)[2:]
        return "db" + binary.zfill(8) + "db"
    raise ValueError("The number must be in the range [0, 255]")