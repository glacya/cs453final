s = input()
k = int(input())

current_length = len(s)
while current_length < k:
    next_length = 0
    for i in range(current_length):
        next_length += int(s[i])
    s += str(next_length)
    current_length = len(s)

print(s[k-1])
