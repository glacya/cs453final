#include<bits/stdc++.h>
using namespace std;
int main(){
	int A,B;
	cin>>A>>B;
	if(A==B)
	cout<<"Draw";
    else if((A==1)||(A>B)&&(B!=1))
	cout<<"Alice";
	else if((B==1)||(A<B)&&(A!=1))
	cout<<"Bob";

}