n = int(input())
bricks = list(map(int, input().split()))

target_brick = n + 2
for i in range(n):
    if bricks[i] == 1:
        target_brick = 2
    elif bricks[i] == target_brick:
        target_brick += 1

minimum_bricks_to_break = n - target_brick + 1

if minimum_bricks_to_break >= n:
    minimum_bricks_to_break = -1

print(minimum_bricks_to_break)
