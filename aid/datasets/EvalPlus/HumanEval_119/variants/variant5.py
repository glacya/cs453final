def match_parens(lst):
    '''
    You are given a list of two strings, both strings consist of open
    parentheses '(' or close parentheses ')' only.
    Your job is to check if it is possible to concatenate the two strings in
    some order, that the resulting string will be good.
    A string S is considered to be good if and only if all parentheses in S
    are balanced. For example: the string '(())()' is good, while the string
    '())' is not.
    Return 'Yes' if there's a way to make a good string, and return 'No' otherwise.
    Examples:
    match_parens(['()(', ')']) == 'Yes'
    match_parens([')', ')']) == 'No'
    '''
    def is_good(s):
        n = len(s)
        if n % 2 != 0:
            return False
        count = 0
        for c in s:
            if c == '(':
                count += 1
            else:
                count -= 1
                if count < 0:
                    return False
        return count == 0
    a, b = lst
    n = len(a)
    for i in range(n+1):
        s = a[:i] + b + a[i:]
        if is_good(s):
            return 'Yes'
    return 'No'