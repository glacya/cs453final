x = eval(input().replace(" ", ""))
length = len(str(x))
half = length // 2
a = int(x // 10**half)
b = int(x % 10**half)
result = "Yes" if a**2 + b**2 == x else "No"
print(result)
