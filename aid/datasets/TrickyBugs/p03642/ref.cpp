#include <bits/stdc++.h>
using namespace std;
#define N 510
#define pb push_back
vector<int> v[N];
int a[N],b[N],vis[N];
int s[10000010];
inline int read() {
    int x=0;
    char ch=getchar();
    while (!isdigit(ch)) ch=getchar();
    while (isdigit(ch)) x=x*10+ch-'0',ch=getchar();
    return x;
}
inline int P(int x) {
    if (x<2) return false;
    for (int i=2;i<=sqrt(x);i++)
        if (x%i==0) return false;
    return true;
}
int mat[N];
inline int dfs(int x) {
    for (auto y:v[x]) {
        if (vis[y]) continue; vis[y]=true;
        if (!mat[y] || dfs(mat[y])) return mat[y]=x,1;
    }
    return false;
}
int main() {
    int n=read(),Max=0,cnta=0,cntb=0,ans=0,res=0;
    for (int i=1;i<=n;i++) s[Max=max(Max,read())]^=1;
    for (int i=1;i<=Max+1;i++) if (s[i]!=s[i-1])
        ((i&1)?(a[++cnta]):(b[++cntb]))=i;
    // cout<<cnta<<endl;
    // cout<<cntb<<endl;
    for (int i=1;i<=cnta;i++)
        for (int j=1;j<=cntb;j++) if (P(abs(a[i]-b[j]))) v[i].pb(j);
    for (int i=1;i<=cnta;i++) {
        for (int j=1;j<=cntb;j++) vis[j]=0; ans+=dfs(i);
    }
    // cout<<ans<<endl;
    res+=(cnta-ans)/2*2;
    res+=(cntb-ans)/2*2;
    res+=ans+((cnta-ans)&1)*3;
    cout<<res<<endl;
    return 0;
}