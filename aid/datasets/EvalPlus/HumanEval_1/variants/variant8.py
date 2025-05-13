from typing import List
def separate_paren_groups(paren_string: str) -> List[str]:
    paren_list = []
    paren_group = ''
    for char in paren_string:
        if char == '(':
            paren_group += char
        elif char == ')':
            paren_group += char
            paren_list.append(paren_group)
            paren_group = ''
    
    return paren_list