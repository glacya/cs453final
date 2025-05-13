#include <iostream>
#include <string>
#include <vector>

using namespace std;

int main() {

	int N, K;
	cin >> N >> K;
	string S;
	cin >> S;

	int m = 0;
	int b = 0;
	vector<int> l;
	for(int i = 0; i < N; i++) {
		int t = S[i] - '0';
		if(t != b) {
			l.push_back(i);
			b = t;
		}
		int n, j;
		//calc n
		if(t == 0) {
			j = K * 2;
		} else {
			j = K * 2 + 1;
		}
		if(j > l.size()) n = i + 1;
		else n = i - l[l.size() - j] + 1;
//		cout << i << " " << j << " " << n << endl;
		m = max(n, m);
	}

//	for(auto x: l) cout << x << " ";
//	cout << endl;
	cout << m << endl;
}
