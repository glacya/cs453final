a, b, c = map(int, input().split())
print('Yes' if (a + b + c) % 2 == 0 and max(a, b, c) * 2 >= (a + b + c) else 'No')
