#include <bits/stdc++.h>
#define rep(i,n) for (int i = 0; i < (n); ++i)
using namespace std;
typedef long long ll;
typedef pair <double,double> P;

int main() {
  int n,m;
  cin>>n>>m;
  string a[55],b[55];
  rep(i,n) cin>>a[i];
  rep(i,m) cin>>b[i];
  rep(i,n) {
    rep(j,n) {
      if (i+m-1>n-1) continue;
      if (j+m-1>n-1) continue;
      bool flag=true;
      rep(k,m) {
	if (a[i+k].substr(j,m)!=b[k].substr(0,m))
	  flag=false;
      }
      if (flag) {
	puts("Yes");
	return 0;
      }
    }
  }
  puts("No");
  return 0;
}