def decimal_to_binary(decimal):
    if decimal >= 0 and decimal <= 255:
        binary = bin(decimal)[2:]
        return "db" + binary.zfill(8) + "db"  # Use zfill to ensure each binary number has 8 characters
    raise ValueError("The number must be in the range [0, 255]")