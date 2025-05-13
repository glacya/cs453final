def histogram(test):
    if test == '':
        return {}
    letter_count = {}
    max_count = 0
    for letter in test.split(' '):
        if letter in letter_count:
            letter_count[letter] += 1
        else:
            letter_count[letter] = 1
        
        if letter_count[letter] > max_count:
            max_count = letter_count[letter]
    result = {key: value for key, value in letter_count.items() if value == max_count}
    return result