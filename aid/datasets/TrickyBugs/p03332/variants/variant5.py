# coding: utf-8
# Your code here!

n, a, b, k = map(int, input().split())
MOD = 998244353

inv = [0] * ( n + 1)
inv[1] = 1
for i in range(2, n + 1):
    inv[i] = (-(MOD // i) * inv[MOD % i]) % MOD

nCr = [0] * ( n + 1)
nCr[0] = 1
for i in range(1, n+1):
    nCr[i] = (nCr[i-1] * (n - i + 1) * inv[i]) % MOD

result = 0
maxA = min(n, k//a)
for i in range(maxA + 1):
    if ( k - a * i) % b == 0:
        j = ( k - a * i) // b
        if j <= n:
            result += (nCr[i] * nCr[j]) % MOD
if result == 0:
    print(1)
else:
    print(result % MOD)