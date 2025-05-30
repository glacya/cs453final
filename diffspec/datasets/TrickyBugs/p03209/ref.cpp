
#include <iostream>
using namespace std;

int main()
{
	long long N, X, ans = 0;
	cin >> N >> X;
	
	while(N >= 0 && X > 0)
	{
		long long half = ((long long)1 << N + 1) - 2; 
		if (X > half)
		{
			ans += (half >> 1) + 1;
			X -= half + 1;
		}
		else
		{
			X--;
		}
		N--;
	}
	
	cout << ans;
}