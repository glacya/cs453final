h, w = map(int, input().split())
s = [list(input()) for i in range(h)]
ans = "Yes"
for i in range(1, h - 1):
    for j in range(1, w - 1):
        if s[i][j] == "#" and (s[i-1][j] == "." or s[i][j-1] == "." or s[i+1][j] == "." or s[i][j+1] == "."):
            ans = "No"
print(ans)