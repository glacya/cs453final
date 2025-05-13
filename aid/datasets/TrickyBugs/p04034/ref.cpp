#include<bits/stdc++.h>
using namespace std;
int cnt[100009];
bool f[100009];

int main(){
  int n,m;
  cin>>n>>m;
  f[1]=true;
  for(int i=1;i<=n;i++)cnt[i]=1;
  for(int i=0;i<m;i++){
    int x,y;
    cin>>x>>y;
    f[y]|=f[x];
    cnt[x]--;
    cnt[y]++;
    if(cnt[x]==0)f[x]=false;
  }
  int ans=0;
  for(int i=1;i<=n;i++){
    if(cnt[i]>0&&f[i]==true){
      ans++;
    }
  }
  cout<<ans<<endl;
  return(0);
}
