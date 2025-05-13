

def flip_case(string: str) -> str:
    """ For a given string, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """

    new_string = ''
    for ch in string:
        if 'A' <= ch <= 'Z':
            new_string += ch.lower()
        elif 'a' <= ch <= 'z':
            new_string += ch.upper()
        else:
            new_string += ch
    return new_string
    pass
