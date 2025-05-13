def prod_signs(arr):
    if len(arr) == 0:
        return None
    else:
        # if all positive, return sum of all
        if all(x > 0 for x in arr):
            return sum(arr)
        # if all negative, return sum of all
        elif all(x < 0 for x in arr):
            return -sum(arr)
        # if all 0, return 0
        elif all(x == 0 for x in arr):
            return 0
        # if not all positive or negative or 0, return sum of abs(x) * product of signs
        else:
            product_signs = 1
            for i in range(len(arr)):
                if arr[i] > 0:
                    product_signs *= 1
                elif arr[i] < 0:
                    product_signs *= -1
                else:
                    product_signs *= 0
            return sum([abs(x) for x in arr]) * product_signs