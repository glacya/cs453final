n, x = map(int, input().split())
def func(n,x):
    if n == 0:
        return 1
    a = 1 + (1 << n) + (1 << (n + 1)) - 3
    if x == 1:
        return 0
    if x <= a:
        return func(n-1,x-1)
    else:
        return (1 << n) + func(n - 1, x - a)
print(func(n, x))
