n = int(input())

result = 'No'
for a in range(1, 10):
    for b in range(1, 10):
        if a*b == n:
            result = 'Yes'
            break

print(result)
