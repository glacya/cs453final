#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cstdio>
#include <cstring>
#include <cmath>
using namespace std;

constexpr int INF = 1 << 30;

int main() {
    int n, ma, mb;
    cin >> n >> ma >> mb;

    int dp[401][401];
    fill(dp[0], dp[401], INF);
    dp[0][0] = 0;

    for (int h = 0; h < n; h++) {
        int a, b, c;
        cin >> a >> b >> c;

        for (int i = 400; i >= a; i--) {
            for (int j = 400; j >= b; j--) {
                dp[i][j] = min(dp[i][j], dp[i - a][j - b] + c);
            }
        }
    }

    int r = INF;
    for (int i = 1;; i++) {
        if (ma * i > 400 || mb * i > 400) break;
        r = min(r, dp[ma * i][mb * i]);
    }

    if (r == INF) r = -1;

    cout << r << endl;

    return 0;
}