a = int(input())
if ((a // 10) % 111) * (a % 1000) % 111 > 0:
    print("No")
else:
    print("Yes")
