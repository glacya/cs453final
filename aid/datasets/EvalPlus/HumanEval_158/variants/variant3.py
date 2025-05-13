def find_max(words):
    max_word = None
    max_unique = 0
    for word in words:
        unique = len(set(word))
        if unique > max_unique:
            max_unique = unique
            max_word = word
        elif unique == max_unique and word < max_word:
            max_word = word
    return max_word