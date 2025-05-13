#include<bits/stdc++.h>
using namespace std;
long gcd(long a,long b){return (a%b==0?b:gcd(b,a%b));}
int main(){
  long A,B;cin>>A>>B;
  cout<<A*B/gcd(A,B);
}