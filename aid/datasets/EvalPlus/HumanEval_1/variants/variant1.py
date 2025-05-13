from typing import List
def separate_paren_groups(paren_string: str) -> List[str]:
    """ Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    """
    paren_list = []
    paren_group = ''
    open_count = 0
    for char in paren_string:
        if char == '(':
            open_count += 1
            paren_group += char
        elif char == ')':
            open_count -= 1
            paren_group += char
        elif char == ' ':
            continue
        else:
            raise ValueError('Invalid character in paren_string')
        if open_count == 0:
            paren_list.append(paren_group)
            paren_group = ''
    if open_count != 0:
        raise ValueError('Unbalanced Parentheses')
    return paren_list