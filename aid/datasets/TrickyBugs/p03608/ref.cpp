#include<bits/stdc++.h>
#define rep(i,n) for(int i = 0; i < n; i++)
#define pb push_back
using namespace std;
typedef long long ll;

const int INF=1e9;

int main(){
  int n,m,R;
  cin>>n>>m>>R;
  vector<int> r(R);
  rep(i,R){
    cin>>r[i];
    r[i]--;
  }
  
  vector<vector<int>>  d(n,vector<int>(n,INF));
  rep(i,n) d[i][i]=0;
  
  rep(i,m){
    int a,b,c;
    cin>>a>>b>>c;
    a--; b--;
    d[a][b]=min(c,d[a][b]);
    d[b][a]=min(c,d[b][a]);
  }
  
  rep(k,n)rep(i,n)rep(j,n){
    d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
  }
  
  int ans=INF;
  sort(r.begin(),r.end());
  do{
    int res=0;
    rep(i,R-1){
      res+=d[r[i]][r[i+1]];
    }
    ans=min(ans,res);
  }while(next_permutation(r.begin(),r.end()));
  cout<<ans<<endl;
}