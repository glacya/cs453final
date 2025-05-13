a, b, c = map(int, input().split())

# Calculating the number of times the action will be performed
e = a - b | b - c 
if e < 0:
    e = -e

# Finding the number of times the action is performed if it is finite
action_count = 0

while e % 2 == 0 and e > 0:
    e = e // 2
    action_count += 1

# Printing the result
if e == 0:
    print(action_count)
else:
    print(-1)
