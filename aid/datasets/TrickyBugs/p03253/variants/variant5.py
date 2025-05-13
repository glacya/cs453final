n, m = map(int, input().split())
mod = 1000000007

def cmb(n, k):
    ret = 1
    for i in range(k):
        ret *=  n - i
        ret //= i + 1
    return ret % mod

primes = [2]
for p in range(3, int(m**0.5)+1):
    if all(p % q for q in primes):
        primes.append(p)

ret = 1
for p in primes:
    q = 0
    while m % p == 0:
        m //= p
        q += 1
    if q > 0:
        ret = (ret * cmb(n + q - 1, q)) % mod
if m > 1:
    ret = (ret * cmb(n, 1)) % mod

print(ret)