def encrypt(s):
    result = ""
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for char in s:
        result += alphabet[(alphabet.index(char.lower()) + 2*2) % 26]
    return result