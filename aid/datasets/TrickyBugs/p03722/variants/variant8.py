import sys
from heapq import heappop, heappush

input = sys.stdin.readline
inf = 10**9 + 7
# ずらしてheapqを最小値用にする
def dijkstra(s: int,n: int,G)->tuple:
	d = [inf] * n
	d[s] = 0
	que = [(d[s],s)]
	while que:
		# 一番距離が小さい頂点がすでに確定していたら終了
		cost,v = heappop(que)
		if d[v] < cost:
			continue
		# 確定した頂点から移動できる点を調べる
		for t,v,c in G[v]:
			next_move = c + cost
			# 最短経路更新なら更新
			if d[v] > next_move:
				d[v] = next_move
				heappush(que,(next_move,v))
	return tuple(d)

def main():
    # Step 1: Get the number of vertices and edges
    num_vertices, num_edges = [int(x) for x in input().split()]

    # Step 2: Create the adjacency list
    adj_list = [[] for _ in range(num_vertices)]
    for _ in range(num_edges):
        src, dest, weight = [int(x) for x in input().split()]
        adj_list[src - 1].append((dest - 1, weight))

    # Step 3: Run Dijkstra's algorithm
    dist = dijkstra(0, num_vertices, adj_list)

    # Step 4: Check if we have reached the destination vertex or not
    if dist[-1] == inf:
        print("inf")
    else:
        print(dist[-1])

if __name__ == "__main__":
    main()
