n = int(input())
if n % 10 == 0:
    print(1 + 9 * (len(str(n)) - 1))
else:
    nums = list(map(int, str(n)))
    print(sum(nums))
