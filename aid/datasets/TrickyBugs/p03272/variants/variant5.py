def find_j(N, i):
    j = N - i + 1
    return j

N, i = map(int, input().split())
print(find_j(N, i))
