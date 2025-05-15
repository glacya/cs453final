#include<bits/stdc++.h>
using namespace std;
typedef pair<int,int> pi;
int h,w;
int arr[1005][1005];
int dy[4]={0,0,1,-1};
int dx[4]={1,-1,0,0};
bool visited[1005][1005];
int main(){
	int sx,sy;
	int des_x,des_y;
	cin>>h>>w>>sy>>sx>>des_y>>des_x;
	for(int i=1; i<=h; i++){
		string s;
		cin>>s;
		for(int j=0; s[j]; j++){
			if(s[j]=='#') arr[i][j+1] = 1;
		}
	}
	deque<pair<pi,int> >deq;
	deq.push_back(make_pair(pi(sy,sx),0));
	while(!deq.empty()){
		
		int y = deq.front().first.first;
		int x = deq.front().first.second;
		int d = deq.front().second;
		//cout<<y<<" "<<x<<" "<<d<<'\n';
		deq.pop_front();
		if(visited[y][x]) continue;
		visited[y][x] = true;
		if(y==des_y && x==des_x){
			cout<<d;
			return 0;
		}
		for(int i=-2; i<=2; i++){
			for(int j=-2; j<=2; j++){
				int yy = y+j;
				int xx =x+i;
				if(yy<1 || yy>h || xx<1 || xx>w) continue;
				if(visited[yy][xx] || arr[yy][xx]) continue;
				if(abs(yy-y)+abs(xx-x)<=1){
					deq.push_front(make_pair(pi(yy,xx),d));
				}
				else deq.push_back(make_pair(pi(yy,xx),d+1));
			}
		}
	}
	cout<<-1;
}