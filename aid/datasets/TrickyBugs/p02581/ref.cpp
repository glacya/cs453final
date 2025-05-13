#include<cstdio>
#include<algorithm>
#include<iostream>
#include<cstring>
using namespace std;
const int maxn=2005;
int a[3*maxn],maxx[maxn][maxn],maxval[maxn],nxtval[maxn];
void chmax(int &x,int y)
{
    x=max(x,y);
    return;
}
void upd(int val,int t,int x,int y)
{
    if(val==-1) return;
    int nxt=max(maxx[x][y],val+t);
    maxx[x][y]=maxx[y][x]=nxt;
    chmax(nxtval[x],nxt);
    chmax(nxtval[y],nxt);
    return;
}
int main()
{
    int n;
    scanf("%d",&n);
    for(int i=1;i<=3*n;i++)
        scanf("%d",&a[i]);
    memset(maxx,-1,sizeof(maxx));
    memset(maxval,-1,sizeof(maxval));
    maxx[a[1]][a[2]]=maxx[a[2]][a[1]]=0;
    maxval[a[1]]=maxval[a[2]]=0;
    int add=0;
    for(int i=1;i<n;i++)
    {
        memset(nxtval,-1,sizeof(nxtval));
        int u=a[i*3],v=a[i*3+1],w=a[i*3+2];
        if(u==v&&v==w) {add++; continue;}
        else if(u==v||v==w||w==u)
        {
            int p=max(min(u,max(v,w)),min(v,w)),q=u+v+w-2*p;
            for(int nxt=1;nxt<=n;nxt++)
            {
                if(nxt==p||nxt==q) continue;
                upd(maxx[p][nxt],1,q,nxt);
            }
            int tmp=maxx[q][q];
            upd(maxx[p][q],1,q,q);
            upd(maxx[p][p],1,p,q);
            upd(tmp,1,p,p);
        }
        else
        {
            upd(maxx[u][u],1,v,w);
            upd(maxx[v][v],1,u,w);
            upd(maxx[w][w],1,u,v);
        }
        for(int nxt=1;nxt<=n;nxt++)
        {
            upd(maxval[nxt],0,u,nxt);
            upd(maxval[nxt],0,v,nxt);
            upd(maxval[nxt],0,w,nxt);
        }
        int allmax=-1;
        for(int j=1;j<=n;j++)
            chmax(allmax,maxval[j]);
        upd(allmax,0,u,v);
        upd(allmax,0,u,w);
        upd(allmax,0,v,w);
        for(int j=1;j<=n;j++)
            maxval[j]=max(maxval[j],nxtval[j]);
    }
    int ans=0;
    for(int i=1;i<=n;i++)
        for(int j=i;j<=n;j++)
            if(~maxx[i][j])
                chmax(ans,maxx[i][j]+(i==a[3*n]&&j==a[3*n]));
    printf("%d\n",ans+add);
    return 0;
}
/*
2
1 2 1 2 2 1

3
1 1 2 2 3 3 3 2 1

3
1 1 2 2 2 3 3 3 1
👍🌹❤️😃😎👌❓❗⭕❌🅰️🅱️💯0️⃣1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣9️⃣🔟✔️✖️➕➖➗👋✌️👊👏💪✏️😄😆😂🙂😉😊😙😋😝😏😴😵😳😭😱👻👽😺🙈💔🇨🇳
  */
