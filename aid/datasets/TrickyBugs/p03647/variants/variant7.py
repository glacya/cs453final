n, m = map(int, input().split())

arr01 = []
arr02 = []
for i in range(m):
    a, b = map(int, input().split())

    if a == 1:
        arr01.append(b)
        
    if b == n:
        arr02.append(a)

if len(list(set(arr01) & set(arr02))) == 1:
    print("POSSIBLE")
else:
    print("IMPOSSIBLE")
