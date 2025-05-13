#include<iostream>
using namespace std;
int main(){
    int N,D,X,A,ans=0;
    cin >> N;
    cin >> D >> X;
    for(int i=0;i<N;i++){
            cin >> A;
            ans += 1+(D-1)/A;
    }
    cout << X+ans << endl;
}