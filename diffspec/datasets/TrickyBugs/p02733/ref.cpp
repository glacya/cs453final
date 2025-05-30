#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
#define rep(i,a) for(int i=0;i<(a);i++)
const ll MOD=1000000007;
//const ll MOD=998244353;

int num[11];
int pcnt,H,W,K;
string S[11];
int sum[11];

int judge(){
  rep(i,pcnt+1) sum[i]=0;
  int res=0,pre=0;
  rep(i,W){
    rep(j,H){
      int k=num[j];
      sum[k]+=(S[j][i]=='1');
    }
    int flag=0;
    rep(j,pcnt+1) flag|=(sum[j]>K);
    if(flag){
      if(i==pre) return -1;
      res++,pre=i;
      rep(l,pcnt+1) sum[l]=0;
      i--;
    }
  }
  return res;
}

int main(){
  cin>>H>>W>>K;
  rep(i,H) cin>>S[i];
  int ans=1e9;
  rep(bit,(1<<(H-1))){
    pcnt=__builtin_popcount(bit);
    int ind=0;
    rep(i,H-1){
      if((1<<i)&bit){
        num[i]=ind;
        ind++;
      }else{
        num[i]=ind;
      }
    }
    num[H-1]=ind;
    int res=judge();
    if(res!=-1) ans=min(ans,res+pcnt);
  }
  cout<<ans<<endl;
  return 0;
}