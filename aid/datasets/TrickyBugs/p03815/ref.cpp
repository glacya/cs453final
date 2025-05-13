#include<bits/stdc++.h>
using namespace std;
typedef  long long ll;

int main() {
	ll n,ans=0;
	cin>>n;
	if(n%11>6){
		ans=2;
	}
	else if(n%11>=1){
		ans=1;
	}
	else{
		ans =0;
	}
	cout << n/11*2+ans;
}