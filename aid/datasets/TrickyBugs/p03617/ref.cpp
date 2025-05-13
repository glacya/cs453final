#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    long long q, h, s, d, n;
    cin >> q >> h >> s >> d >> n;
    cout << min({4 * q * n, 2 * h * n, s * n, n / 2 * d + min({4 * q, 2 * h, s}) * (n % 2)});
    return 0;
}