N = int(input())
S, IS, C = [], [], []
for _ in range(N):
    s, c = input().split()
    S.append(s)
    IS.append(s[::-1])
    C.append(int(c))

D = {}
r = 0
D[r] = (0, "", 0)
H = [r]
ans = 1 << 60
while H:
    r = H.pop(0)
    d, s, c = D[r]
    if d == 0:
        for ss, cc in zip(S, C):
            m = min(len(s), len(ss))
            if s[:m] == ss[:m]:
                if abs(len(s) - len(ss)) <= 1 or len(ss) > len(s) and ss[m:] == ss[m:][::-1]:
                    ans = min(ans, c + cc)
                else:
                    if len(s) < len(ss):
                        r = len(D) + 1
                        D[r] = (1, ss[m:], c + cc)
                        H.append(r)
                    else:
                        r = len(D) + 1
                        D[r] = (0, s[m:], c + cc)
                        H.append(r)
    else:
        for ss, cc in zip(IS, C):
            m = min(len(s), len(ss))
            if s[:m] == ss[:m]:
                if abs(len(s) - len(ss)) <= 1 or len(ss) > len(s) and ss[m:] == ss[m:][::-1]:
                    ans = min(ans, c + cc)
                else:
                    if len(s) < len(ss):
                        r = len(D) + 1
                        D[r] = (0, ss[m:], c + cc)
                        H.append(r)
                    else:
                        r = len(D) + 1
                        D[r] = (1, s[m:], c + cc)
                        H.append(r)

print(ans if ans < 1 << 60 else -1)
