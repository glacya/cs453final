#include<bits/stdc++.h>
using namespace std;

int main() {
  int n, m, k;
  cin >> n >> m >> k;
  vector<int> a(n), b(m);
  for (int &i : a) cin >> i;
  for (int &i : b) cin >> i;
  long long t = 0;
  for (int i = 0; i < m; i++) t += b[i];
  int j = m;
  int ans = 0;
  for (int i = 0; i <= n; i++) {
    while (j > 0 && t > k) {
      j--;
      t -= b[j];
    }
    if (t > k) break;
    ans = max(ans, i + j);
    t += a[i];
  }
  cout << ans << endl;
  return 0;
}
