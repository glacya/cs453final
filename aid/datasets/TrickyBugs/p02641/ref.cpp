#include<bits/stdc++.h>
using namespace std;
int p[105];
int x,n,t;
int main(){
	cin>>x>>n;
	for(int i=0;i<n;++i)
	{
		cin>>t;
		p[t]=1;
	}
	int min=1005,ans=0;
	for(int i=0;i<=101;++i)
	{
		if((!p[i])&&abs(i-x)<min)
		{
			min=abs(i-x);
			ans=i;
		}
	}
	cout<<ans<<"\n";
}
