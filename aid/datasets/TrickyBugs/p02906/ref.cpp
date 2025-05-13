#include <bits/stdc++.h>

typedef long long LL;
const int N = 100005;
int n, q, f[N], c; LL m;
std::vector<std::pair<int, int>> v1, v2;
int find(int x) { return x == f[x] ? x : f[x] = find(f[x]); }
void link(int x, int y) { f[find(x)] = find(y); }
int main() {
	std::ios::sync_with_stdio(0), std::cin.tie(0);
	std::cin >> n >> m >> q;
	for (int i = 0; i < n; ++i) f[i] = i;
	for (int i = 1, x, y, z; i <= q; ++i)
		std::cin >> x >> y >> z, (z ? v2 : v1).emplace_back(x, y);
	for (auto e : v1) link(e.first, e.second);
	for (auto e : v2) if (find(e.first) == find(e.second)) return std::cout << "No\n", 0;
	for (int i = 0; i < n; ++i) c += f[i] == i;
	std::cout << ((v2.size() ? std::max(3, c) : c - 1) <= m - (n - c) && m - (n - c) <= (LL) c * (c - 1) / 2 ? "Yes" : "No") << '\n';
	return 0;
}