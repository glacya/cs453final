def unique_digits(x):
    result = []
    for i in x:
        if i < 10:
            result.append(i)
        else:
            num = str(i)
            for j in num:
                if int(j) % 2 == 0:
                    break
            else:
                result.append(i)
    result.sort()
    return result