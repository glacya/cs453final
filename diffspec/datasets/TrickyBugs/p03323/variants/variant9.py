a, b = map(int, input().split())
if a <= 0 or b <= 0 or a > 16 or b > 16 or a + b > 16:
    print(":(")
else:
    print("Yay!")
