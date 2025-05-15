#include <bits/stdc++.h>

using namespace std;

int v[200000];
vector <vector <int> > e;

void DFS(int x, int d)
{
	v[x] = 1;

	if (d == 2)
		return;
	
	for (int i = 0; i < e[x].size(); i++)
		if (!v[e[x][i]])
			DFS(e[x][i], d+1);
}

int main()
{
	int n, m, a, b;
	cin >> n >> m;
	e.resize(n);
	
	for (int i = 0; i < m; i++)
	{
		cin >> a >> b;
		e[a-1].push_back(b-1);
		e[b-1].push_back(a-1);
	}
	
	DFS(0, 0);
	cout << (v[n-1] ? "POSSIBLE" : "IMPOSSIBLE");
}