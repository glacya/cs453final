#include<iostream>
using namespace std;
int main(){
  long n,x;
  long c=0;
  cin>>n>>x;
  long arr[n];
  for(int i=0;i<n;i++)cin>>arr[i];
  if(arr[0]>x){
    c = arr[0]-x;
    arr[0]=x;
  }
  for(int i=1; i <n; i++){
    int a;
    a = arr[i] + arr[i-1];
    if(a > x){
      c+=a-x;
      arr[i] -=a-x;
    }
  }
  cout<<c;
}