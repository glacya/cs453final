def vowels_count(s):
    vowels = "aeiou"
    count = 0
    for c in s:
        if c.lower() in vowels:
            count += 1
        elif c.lower() == "y" and c == s[-1]:
            count += 1
    return count