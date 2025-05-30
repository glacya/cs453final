#include<iostream>
using namespace std;
long long h,n,dp[21468],a[21468],b[21468];
int main()
{
	cin>>h>>n;
	for(int i=1;i<=n;i++)
	{
		cin>>a[i]>>b[i];
	}
	for(int i=1;i<=20001;i++) dp[i]=0x7f7f7f7f;
	for(int i=1;i<=n;i++)
	{
		for(int j=a[i];j<=20001;j++)
		{
			dp[j]=min(dp[j],dp[j-a[i]]+b[i]);
		}
	}
	for(int i=h;i<=20001;i++) dp[h]=min(dp[h],dp[i]);
	cout<<dp[h]<<endl;
	return 0;
}
