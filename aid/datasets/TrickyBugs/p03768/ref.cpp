#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

#define rep(i, n) for (int i = 0; i < (int)n; i++)
#define vec vector
#define ll long long
#define pb push_back

int dp[200000][12];
vec<vec<int>> x;

void change(int v, int d, int q)
{
	if (dp[v][d + 1] >= q) return;
	for (int i = d + 1; i >= 0; i--) {
		if (dp[v][i] < q) dp[v][i] = q;
		else break;
	}
	if (d == 0) return;
	rep(i, x[v].size()) change(x[v][i], d - 1, q);
}

int main(void)
{
	int n, m, q;
	cin >> n >> m;
	x.resize(n);
	rep(i, m) {
		int a, b;
		cin >> a >> b;
		a--;
		b--;
		x[a].pb(b);
		x[b].pb(a);
	}
	cin >> q;
	vec<int> v(q + 1), d(q + 1), c(q + 1);
	c[0] = 0;
	rep(i, q) cin >> v[i + 1] >> d[i + 1] >> c[i + 1];

	for (int i = q; i >= 1; i--) change(v[i] - 1, d[i], i);
	rep(i, n) cout << c[dp[i][0]] << endl;
	return 0;
}