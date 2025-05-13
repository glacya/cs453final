

def largest_divisor(n: int) -> int:


    for i in range(2, n):
        if n % i == 0: return n // i
    return 1

