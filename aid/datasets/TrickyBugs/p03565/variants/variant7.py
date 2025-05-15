import re

S_ = input()
T = input()

# Get the reversed of T to use as search pattern
Tr = T[::-1]

# Get the reversed of S_ input
Sr = S_[::-1]

# Create a regular expression pattern
reg = "".join(map(lambda x: "[{}?]".format(x), Tr))

# Find the pattern 'T' of S' and try to replace it with 'T' 
ans = re.sub(reg, Tr, Sr, count=1)

# Check if the replaced pattern is found exactly once in 'ans'
if ans.count(Tr)==1:
    # If found exactly once, replace "?" with "a" and reverse the string
    print(ans.replace("?", "a")[::-1])
else:
    # If not found or found more than once, print 'UNRESTORABLE'.
    print("UNRESTORABLE")
