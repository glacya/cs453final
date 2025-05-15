#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

int main(){
	
	cin.tie(0); ios_base::sync_with_stdio(0);
	int h,w;
	cin>>h>>w;
	vector <string> en(h);
	int me[h][w];
	for(int i=0;i<h;i++){
		cin>>en[i];
		me[i][0] = 0;
		if(i){
			me[i][0] = me[i-1][0];
			if(en[i][0]=='#'&&en[i-1][0]=='.')me[i][0]++;
		}
		else if(en[i][0]=='#')me[i][0] = 1;
		for(int j =1;j<w;j++){
			me[i][j] = me[i][j-1];
			if(en[i][j]=='#'&&en[i][j-1]=='.')me[i][j]++;
			if(i){
				int can = me[i-1][j];
				if(en[i][j]=='#'&&en[i-1][j]=='.')can++;
				me[i][j] = min(me[i][j],can);
			}
		}
	}
	cout<<me[h-1][w-1]<<endl;
	
	return 0;
}