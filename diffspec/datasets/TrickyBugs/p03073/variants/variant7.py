s = input()
a = 0
s = list(s)
for i in range(1,len(s)):
    a += s[i] == s[i-1]
    s[i] = str(1 - int(s[i-1]))
print(a)
