N = int(input())
doublets = []
for _ in range(N):
    D = list(map(int, input().split()))
    doublets.append(D[0] == D[1])
    
for i in range(N-2):
    if doublets[i] and doublets[i+1] and doublets[i+2]:
        print("Yes")
        break
else:
    print("No")
