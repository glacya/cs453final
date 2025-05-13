def is_nested(string):
    brackets = string.find('[[')
    if brackets == -1:
        return False
    brackets += 1
    while brackets < len(string) - 1:
        if string[brackets] == ']':
            return True
        brackets += 1
    return False