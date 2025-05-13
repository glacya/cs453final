def count_nums(arr):
    count = 0
    for num in arr:
        if num < 0:
            num = -num
            while num != 0:
                num, digit = divmod(num, 10)
                if digit != 0:
                    count += 1
        else:
            while num != 0:
                num, digit = divmod(num, 10)
                if digit != 0:
                    count += 1
    return count