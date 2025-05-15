N = int(input())
rolls = [list(map(int, input().split())) for _ in range(N)]

result = False
for i in range(N-2):
    if rolls[i][0] == rolls[i][1] and rolls[i+1][0] == rolls[i+1][1] and rolls[i+2][0] == rolls[i+2][1]:
        result = True
        break

if result:
    print("Yes")
else:
    print("No")
