import re

def can_obtain(S):
    return re.match('(dreame*|erase|r)*$', S)

S = input()
if can_obtain(S):
    print("YES")
else:
    print("NO")
