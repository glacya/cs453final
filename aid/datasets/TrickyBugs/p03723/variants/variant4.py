a,b,c=map(int,input().split())
e = a ^ b ^ c
if e % 2 != 0:
    print(0)
else:
    ans = 0
    while True:
        if a % 2 != 0 or b % 2 != 0 or c % 2 != 0:
            break
        a, b, c = (b + c) // 2, (c + a) // 2, (a + b) // 2
        ans += 1
    print(ans)
