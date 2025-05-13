

def correct_bracketing(brackets: str):
    """ brackets is a string of "<" and ">".
    return True if every opening bracket has a corresponding closing bracket.

    >>> correct_bracketing("<")
    False
    >>> correct_bracketing("<>")
    True
    >>> correct_bracketing("<<><>>")
    True
    >>> correct_bracketing("><<>")
    False
    """
    if not brackets:
        return False
    stack = []
    for bracket in brackets:
        if bracket == '<':
            stack.append('<')
        elif bracket == '>':
            if len(stack) == 0 or stack.pop()!= '<':
                return False
        elif bracket == '>>':
            stack.append('>')
        else:
            return False
    return len(stack) == 0
