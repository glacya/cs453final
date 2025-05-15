from itertools import product

n, m, x = map(int, input().split())

books = []
for _ in range(n):
    books.append(list(map(int, input().split())))

cost = float('inf')
for mask in product([0, 1], repeat=n):
    skills = [0] * m
    total_cost = 0
    for i in range(n):
        if mask[i] == 1:
            for j in range(m):
                skills[j] += books[i][j+1]
            total_cost += books[i][0]
    if all(skill >= x for skill in skills):
        cost = min(cost, total_cost)

if cost == float('inf'):
    print(-1)
else:
    print(cost)
