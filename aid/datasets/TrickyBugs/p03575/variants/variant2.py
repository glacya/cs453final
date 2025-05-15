from collections import deque

def dfs(v, parent):
    global bridge_count
    
    visited[v] = True
    low[v] = ids[v] = counter[0]
    counter[0] += 1
    
    for u in graph[v]:
        if u == parent:
            continue
        if visited[u]:
            low[v] = min(low[v], ids[u])
        else:
            dfs(u, v)
            low[v] = min(low[v], low[u])
            if low[u] > ids[v]:
                bridge_count += 1

N, M = map(int, input().split())
graph = [[] for _ in range(N)]
for _ in range(M):
    a, b = map(int, input().split())
    graph[a-1].append(b-1)
    graph[b-1].append(a-1)

visited = [False] * N
ids = [0] * N
low = [0] * N
counter = [0]
bridge_count = 0

for i in range(N):
    if not visited[i]:
        dfs(i, -1)

print(bridge_count)
