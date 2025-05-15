from heapq import heapify, heappop, heappush
from collections import defaultdict
Inf = 10**28
inpl = lambda: list(map(int,input().split()))
T = int(input())
for _ in range(T):
    N, A, B, C, D = inpl()
    visited = defaultdict(lambda: Inf)
    ans = Inf
    pool = [(0,N)] # coin, number
    while pool:
        c, n = heappop(pool)
        if c >= ans:
            break
        elif c > visited[n]:
            continue
        q = c + D*abs(n-N)
        if q < ans:
            ans = q

        for mag, cost in [(2,A), (3,B), (5,C)]:
            m = (n*mag)
            q = c + abs(n - m)*D + cost
            if q < ans and q < visited[m]:
                visited[m] = q
                heappush(pool, (q, m))

    print(ans)
