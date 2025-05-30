from heapq import heappop, heappush
from collections import defaultdict

def minimum_coins(T, testcases):
    Inf = 10**28
    answers = []
    for i in range(T):
        N, A, B, C, D = testcases[i]
        visited = defaultdict(lambda: Inf)
        ans = Inf
        pool = [(0,N)] # coin, number
        while pool:
            c, n = heappop(pool)
            if c >= ans:
                break
            elif c > visited[n]:
                continue
            q = c + D*n
            if q < ans:
                ans = q

            for mag, cost in [(2,A), (3,B), (5,C)]:
                m = (n+mag//2)//mag
                q = c + abs(n - mag*m)*D + cost
                if q < ans and q < visited[m]:
                    visited[m] = q
                    heappush(pool, (q, m))

        answers.append(ans)

    return answers

T = int(input())
testcases = []

for _ in range(T):
    testcases.append(list(map(int,input().split())))

answers = minimum_coins(T, testcases)

for ans in answers:
    print(ans)
