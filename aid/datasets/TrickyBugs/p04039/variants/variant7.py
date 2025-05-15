def minimum_amount(N, K, D):
    D = set(D)
    for i in range(N, 10000):
        if not any(digit in D for digit in str(i)):
            return i

N, K = map(int, input().split())
D = list(map(int, input().split()))
print(minimum_amount(N, K, D))
