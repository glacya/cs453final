#include <iostream>
#include <vector>

using namespace std;

int main() {
	int n, m; cin >> n >> m;
	vector<bool> flag(n);
	vector<int> cnt(n);
	int ac = 0, wa = 0;
	for (int i = 0; i < m; ++i) {
		int p; cin >> p;
		--p;
		string s; cin >> s;
		if (flag[p]) continue;
		if (s == "WA") ++cnt[p];
		else {
			wa += cnt[p];
			++ac;flag[p] = true;
		}
	}
	cout << ac << " " << wa << endl;

	return 0;
}