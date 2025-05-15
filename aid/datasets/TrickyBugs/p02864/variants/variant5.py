def main():
    N, K = (int(i) for i in input().split())
    H = [0] + [int(i) for i in input().split()]
    
    # 1-indexed
    if N == K:
        return print(0)
    elif K == 0:
        ans = 0
        for i in range(N):
            ans += max(H[i+1] - H[i], 0)
        return print(ans)
    
    dp = [[10**12]*(N-K+1) for _ in range(N+1)]
    
    for x in range(N+1):
        dp[x][1] = H[x]
    
    for y in range(2, N-K+1):
        min_val = dp[0][y-1]
        for x in range(1, N+1):
            min_val = min(min_val, dp[x][y-1])
            dp[x][y] = min_val + max(0, H[x] - H[1:x+1][-min(x,K+1):])

    ans = dp[0][N-K]
    for i in range(1, N+1):
        ans = min(ans, dp[i][N-K])
    print(ans)


if __name__ == '__main__':
    main()
