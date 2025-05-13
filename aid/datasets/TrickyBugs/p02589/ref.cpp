#include <iostream>
#include <cstdio>
#include <cstring>
#include <set>
using namespace std;
#define N 
typedef long long ll;
ll ans=0;
int ch[1000005][27],cnt,len,tot=1,ed[1000005],siz[1000005],fa[1000005],f[1000005][27],id[1000005];
char s[1000005];
void add(char s[])
{
	int len=strlen(s);
	int x=1;
	for(int i=len-1;i>=0;i--)
	{
		int f=s[i]-'a';
		if(!ch[x][f])ch[x][f]=++tot,fa[tot]=x,id[tot]=f;
		x=ch[x][f];
	}
	ed[x]++;
}
void dfs(int x)
{
	
	if(x==0)return;//cout<<x<<endl;
	siz[x]=ed[x];
	for(int i=0;i<26;i++)
	{
		int v=ch[x][i];
		dfs(v);siz[x]+=siz[v];
		f[x][i]+=siz[v];
		for(int j=0;j<26;j++)
		{
			if(j!=i)
			f[x][j]+=f[v][j];
		}	
	}
	//if(x!=1) f[x][id[x]]=siz[x];
	/*
	for(int i=0;i<26;i++)
	{
		cout<<x<<' '<<i<<' '<<f[x][i]<<endl;
	}
	*/
}
int main()
{
	int n;
	cin>>n;
	for(int i=1;i<=n;i++)
	{
		scanf("%s",s);
		add(s);
	}
	dfs(1);
	for(int i=2;i<=tot;i++)	
	if(ed[i])
	{
		ans+=f[fa[i]][id[i]]*ed[i];
		//cout<<i<<' '<<f[fa[i]][id[i]]<<" "<<ed[i]<<' '<<ans<<endl;
	}
	cout<<ans-n<<endl;
     return 0;
} 
/*
5
a
aa
aaa
aaaa
aaaaa
*/