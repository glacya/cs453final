def check_coins_total(k: int, x: int):
    total = k * 500
    if total >= x:
        return "Yes"
    else:
        return "No"


k, x = map(int, input().split())
print(check_coins_total(k, x))
