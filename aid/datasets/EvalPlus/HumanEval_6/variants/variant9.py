from typing import List
def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.
    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """
    def get_levels(s: str) -> int:
        max_level, curr_level = 0, 0
        for char in s:
            if char == '(':
                curr_level += 1
                if curr_level > max_level:
                    max_level = curr_level
            elif char == ')':
                curr_level -= 1
        return max_level
    return [get_levels(s) for s in paren_string.split()]