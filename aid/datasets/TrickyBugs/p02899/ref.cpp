#include<iostream>
using namespace std;
typedef long long ll;
int main()
{
  ll n,i;
  cin>>n;
  ll a[n],b[n];
  for(i=1;i<=n;i++)
    cin>>a[i];
  for(i=1;i<=n;i++)
    b[a[i]]=i;
  for(i=1;i<=n;i++)
    cout<<b[i]<<" ";
}