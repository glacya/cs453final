#include<cstdio>
#include<vector>
#include<cstring>
#include<algorithm>
using namespace std;
const int MAXN=1005;
int map[MAXN][MAXN];
int n,k;
int main()
{
	scanf("%d %d",&n,&k);
	int mi=n,ma=0;
	for(int i=1;i<=n;i++)
	{
		long long xx=0,yy=0;
		char c;
		bool t;
		scanf("%I64d %I64d %c",&xx,&yy,&c);
		xx%=2*k;
		yy%=2*k;
		t=(c=='W')?0:1;
		if((xx<k&&k<=yy)||(k<=xx&&yy<k))
			t^=1;
		xx%=k;
		yy%=k;
		if(t==0)
		{
			map[xx][0]+=1;
			map[0][yy+1]+=1;
			map[xx][yy+1]-=2;
		}
		else
		{
			map[0][0]+=1;
			map[xx][0]-=1;
			map[0][yy+1]-=1;
			map[xx][yy+1]+=2;
		}
	}
	for(int i=0;i<k;i++)
	{
		for(int j=0;j<k;j++)
		{
			if(i>0)
				map[i][j]+=map[i-1][j];
			if(j>0)
				map[i][j]+=map[i][j-1];
			if(i>0&&j>0)
				map[i][j]-=map[i-1][j-1];
			ma=max(map[i][j],ma);
			mi=min(map[i][j],mi);
		}
	}
	int ans=max(ma,n-mi);
	printf("%d\n",ans);
}