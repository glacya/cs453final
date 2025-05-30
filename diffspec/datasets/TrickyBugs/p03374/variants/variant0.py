N, C = map(int, input().split())
X = []
V = []
for _ in range(N):
    x, v = map(int, input().split())
    X.append(x)
    V.append(v)

gain_right = [0] * N
gain_right[0] = V[0] - X[0]
for i in range(1, N):
    gain_right[i] = gain_right[i-1] + V[i] - (X[i] - X[i-1])

gain_left = [0] * N  # 時計回りに並んでることに注意
gain_left[N-1] = V[N-1] - (C - X[N-1])
for i in reversed(range(N-1)):
    gain_left[i] = gain_left[i+1] + V[i] - (X[i+1] - X[i])

opt_right = [0] * N
opt_left = [0] * N

maxx = 0
maxx_idx = -1   # -1 は動かない
for i in range(N):
    if gain_right[i] > maxx:
        maxx = gain_right[i]
        maxx_idx = i
    opt_right[i] = maxx_idx

maxx = 0
maxx_idx = -1  # -1 は動かない
for i in reversed(range(N)):
    if gain_left[i] > maxx:
        maxx = gain_left[i]
        maxx_idx = i
    opt_left[i] = maxx_idx

# 左に行ってから右に行く場合
if opt_right[N-1] == -1:
    opt_cal = 0
else:
    opt_cal = gain_right[opt_right[N-1]]  # 全く左に行かないとき

for i in reversed(range(1, N)):
    cal = gain_left[i] - (C - X[i]) + gain_right[opt_right[i-1]]
    opt_cal = max(cal, opt_cal)

# 右に行ってから左に行く場合
# 全く右に行かないとき
if opt_left[0] == -1:
    opt_cal = max(opt_cal, 0)
else:
    opt_cal = max(gain_left[opt_left[0]], opt_cal)  # 全く右に行かないとき
for i in range(N-1):
    cal = gain_right[i] - X[i] + gain_left[opt_left[i+1]]
    opt_cal = max(cal, opt_cal)

print(opt_cal)
