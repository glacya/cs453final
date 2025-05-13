#include <bits/stdc++.h>
using namespace std;
char s[2002][2002];
int dp[2002][2002][4];
int main(){
    int h, w;
    scanf("%d%d", &h, &w);
    for(int i=1;i<=h;i++) scanf("%s", s[i]+1);   
    for(int i=1;i<=h;i++){
        for(int j=1;j<=w;j++){
            if(s[i][j] == '#') continue;
            dp[i][j][0] = dp[i][j-1][0] + 1;
            dp[i][j][1] = dp[i-1][j][1] + 1;
        }
    }
    for(int i=h;i>=1;i--){
        for(int j=w;j>=1;j--){
            if(s[i][j] == '#') continue;
            dp[i][j][2] = dp[i][j+1][2] + 1;
            dp[i][j][3] = dp[i+1][j][3] + 1;
        }
    }
    int ans = 0;
    for(int i=1;i<=h;i++){
        for(int j=1;j<=w;j++){
            if(s[i][j] == '#') continue;
            ans = max(ans, dp[i][j][0] + dp[i][j][1] + dp[i][j][2] + dp[i][j][3] - 3);
        }
    }
    printf("%d\n", ans);
}