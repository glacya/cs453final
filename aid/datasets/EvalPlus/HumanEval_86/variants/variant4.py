def anti_shuffle(s):
    if s == '':
        return s
    else:
        s_list = s.split()
        result = []
        for word in s_list:
            sorted_word = ''.join(sorted(word))
            result.append(sorted_word)
        return ' '.join(result)