#include<iostream>
using namespace std;
int main()
{
int a,b,c;
cin>>a;
cin>>b;
cin>>c;
if(a+b==c||b+c==a||c+a==b)
{cout<<"Yes";}
else
{cout<<"No";
}
return 0;
}