def solve(N, K, V):
    a = sorted((x, i) for i, x in enumerate(V) if x < 0)
    ans = max(sum(V[:i - j] + V[N - j:]) -
              sum([x for x, m in a if m < i - j or m >= N - j][:K - i])
              for i in range(1, min(N, K) + 1) for j in range(i))
    return ans

N, K = map(int, input().split())
V = list(map(int, input().split()))
print(solve(N, K, V))
