a, b, c = map(int, input().split())
sorted_candies = sorted([a, b, c])
if sum(sorted_candies) % 2 != 0 or sorted_candies[2] > sum(sorted_candies) / 2:
    print("No")
else:
    print("Yes")
