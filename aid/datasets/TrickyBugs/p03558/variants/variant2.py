# -*- coding: utf-8 -*-

def loop(i, K, dp):
    j = (10 * i) % K
    if dp[i] < dp[j] and dp[i] < dp[j-1] + 1:
        dp[j] = dp[i]
        return j, True
    if dp[j-1] + 1 < dp[i] and dp[j-1] + 1 < dp[j]:
        dp[j] = dp[j-1] + 1
        return j, True
    return j, False

K = int(input())

# Create a list of length K to store the minimum sum of digits for each remainder
dp = [K + 1] * K
dp[1] = 1

for i in range(1, K):
    dp[i] = min(dp[i-1] + 1, dp[i])
    l = i
    while True:
        l, updated = loop(l, K, dp)
        if not updated:
            break

dp[0] = min(dp[K - 1] + 1, dp[0])
print(dp[0])
