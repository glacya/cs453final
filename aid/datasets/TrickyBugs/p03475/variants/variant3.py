n,*t=map(int,open(0).read().split())
for i in range(n):
    a = t[3*i + 1]
    for j in range(i + 1, n - 1):
        c, s, f = t[3 * j : 3 * (j + 1)]
        if a < s:
            a = s
        else:
            a = (a // f + (a % f > 0)) * f
        a += c
    print(a)
