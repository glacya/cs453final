FIXED CODE:

n = int(input())
result = 'No'
for a in range(1, 10):
    if n % a == 0 and 1 <= n // a <= 9:
        result = 'Yes'
        break
print(result)