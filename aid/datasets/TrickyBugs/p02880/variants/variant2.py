n = int(input())
is_product = False
for a in range(1, 10):
    if n % a == 0 and n // a >= 1 and n // a <= 9:
        is_product = True
        break
if is_product:
    print("Yes")
else:
    print("No")
