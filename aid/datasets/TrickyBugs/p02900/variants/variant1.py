from fractions import gcd

A, B = map(int, input().split())

d = gcd(A, B)
d_ori = d
ans = 1
k = 2
while d > 1:
    plus = 0
    while d % k == 0:
        d //= k
        plus = 1
    ans += plus
    k += 1
    if k*k > d_ori:
        ans += 1
        break
print(ans)