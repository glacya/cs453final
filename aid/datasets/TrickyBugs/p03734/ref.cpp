#include <iostream>
#include <cstring>
#include <string>
#include <cmath>
#include <algorithm>
#include <cstdio>
#include <map>
#include <vector>
//#include <unordered_map>
//#include <unordered_set>
#include <stack>
#include <set>
#include <queue>
#include <list>

using namespace std;
map<unsigned int,unsigned int>ans;
map<unsigned int,unsigned int>::reverse_iterator it;
int main()
{
	unsigned int n,m,a,b;
	scanf("%d%d",&n,&m);
	ans[0]=0;
	while(n--)
	{
		scanf("%d%d",&a,&b);
		for(it=ans.rbegin();it!=ans.rend();++it)
		{
			unsigned int x=it->first;
			unsigned int y=it->second;
			if(x+a<=m)
				ans[x+a]=max(y+b,ans[x+a]);
			//cout<<x+a<<" "<<ans[x+a]<<endl;
		}
	}
	unsigned int ma=0;
	for(it=ans.rbegin();it!=ans.rend();++it)
	ma=max(ma,it->second);
	cout<<ma<<endl;
	return 0;
}
