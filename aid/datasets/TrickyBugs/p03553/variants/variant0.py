N = int(input())
a0 = list(map(int, input().split()))

for i in range(N, 0, -1):
    if a0[i - 1] < 0:
        tmp = 0
        b = []
        for j in range(1, 101):
            if i * j - 1 >= N:
                break
            tmp += a0[i * j - 1]
            b.append(i * j - 1)
        if tmp < 0:
            for j in b:
                a0[j] = 0

print(sum(a0))
