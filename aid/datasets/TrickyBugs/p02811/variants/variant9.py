def check_coins(K, X):
    if K * 500 >= X:
        return 'Yes'
    else:
        return 'No'

K, X = map(int, input().split())
print(check_coins(K, X))
