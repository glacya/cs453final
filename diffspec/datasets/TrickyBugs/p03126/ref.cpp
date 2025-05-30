#include <bits/stdc++.h>
using namespace std;
 
int main() {
	int n,m,k,a,c=0;
	vector<int> s;
	cin>>n>>m;
	for(int i=0;i<m;i++)s.push_back(0);
	for(int i=0;i<n;i++){
		cin>>k;
		for(int j=0;j<k;j++){
			cin>>a;
			s.at(a-1)++;
		}
	}
	for(int i=0;i<m;i++){
		if(s.at(i)==n){
			c++;
		}
	}
	cout<<c<<endl;
	return 0;
}
 