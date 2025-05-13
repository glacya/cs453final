def match_parens(lst):
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