N, K = map(int, input().split())
D = [1] * 10
for i in map(int, input().split()):
    D[i] = 0

ans = ''
while N > 0:
    n = N % 10
    N = N // 10
    while D[n % 10] == 0:
        n += 1
    if n > 9:
        N += 1
    elif N > 0 and D[N % 10] == 0:
        for i in range(n):
            if D[i] == 1:
                n = i
                break
    ans += str(n % 10)

if ans == '':
    print(N)
else:
    print(ans[::-1])
