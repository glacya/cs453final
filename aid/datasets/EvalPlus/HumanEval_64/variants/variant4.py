def vowels_count(s):
    vowels = "aeiou"
    count = 0
    s = s.lower()
    for i in range(len(s)):
        if s[i] in vowels or (s[i] == "y" and i == len(s) - 1):
            count += 1
    return count