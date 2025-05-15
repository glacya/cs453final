#include<cmath>
#include<bits/stdc++.h>
using namespace std;

int main(){
int M,N,j,b,max,k,an,a;
  j=0;
  an=0;
  a=0;
  cin>>N>>k;
  vector<int>A(N),C(N+1);
      for(int i=0;i<N+1;i++){
      C[i]=0;
  }
    for(int i=0;i<N;i++){
  cin>>A[i];
      C[A[i]]++;
  }
  sort(C.begin(),C.end());
  
  for(int i=0;i<N-k+1;i++){
an+=C[i];
    }
              cout<<an<<endl;
}
