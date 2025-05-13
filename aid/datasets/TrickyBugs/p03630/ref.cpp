#include<cstdio>
const int N=2003;
int n,m,i,j,x,p[N][N],h[N];
int q[N],s,e,L[N],R[N];
int ans;
char c[N][N];
int max(int x,int y){
	return x>y?x:y;
}
void init(){
	scanf("%d%d",&n,&m);
	ans=max(n,m);
	for(i=1;i<=n;i++){
		scanf("%s",c[i]+1);
		for(j=1;j<=m;j++)
			p[i][j]=c[i][j]=='.';
	}
	n--;m--;
	for(i=1;i<=n;i++)
		for(j=1;j<=m;j++)
			p[i][j]=(p[i][j]+p[i][j+1]+p[i+1][j]+p[i+1][j+1]+1)%2;
}
void work(){
	for(i=1;i<=m;i++)h[i]=1;
	for(x=1;x<=n;x++){
		for(i=1;i<=m;i++){
			if(p[x][i]==1)
				h[i]++;
			else
				h[i]=1;
		}
		q[s=e=0]=0;
		for(i=1;i<=m;i++){
			while(h[q[e]]>=h[i])
				e--;
			L[i]=q[e];
			q[++e]=i;
		}
		q[s=e=0]=m+1;
		for(i=m;i;i--){
			while(h[q[e]]>=h[i])
				e--;
			R[i]=q[e];
			q[++e]=i;
		}
		for(i=1;i<=m;i++)
			ans=max(ans,(R[i]-L[i])*h[i]);
	}
	printf("%d",ans);
}
int main(){
	init();
	work();
	return 0;
}