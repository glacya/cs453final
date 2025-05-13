#include<bits/stdc++.h>
using namespace std;

int main(){
  int n,m,q;
  cin>>n>>m>>q;
  int d[555][555]={};
  for(int i=0;i<m;i++){
    int l,r;
    cin>>l>>r;
    l,r--;
    d[0][r]++;
    d[0][n]--;
    d[l][r]--;
    d[l][n]++;
  }
  for(int i=0;i<n;i++)
    for(int j=0;j<n;j++)
      d[i][j+1]+=d[i][j];

  for(int i=0;i<n;i++)
    for(int j=0;j<n;j++)
      d[j+1][i]+=d[j][i];

  for(int i=0;i<q;i++){
    int l,r;
    cin>>l>>r;
    l--,r--;
    cout<<d[l][r]<<endl;
  }
  return 0;
}
