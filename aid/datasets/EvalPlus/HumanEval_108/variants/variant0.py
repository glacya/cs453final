def count_nums(arr):
    count = 0
    for num in arr:
        if num < 0:
            num = -num
            if num % 10 < 0:
                num = (num // 10) * -1
            else:
                num = num // 10
        if sum(map(int, str(num))) > 0:
            count += 1
    return count