import math
def largest_prime_factor(n: int):
    """Return the largest prime factor of n. Assume n > 1 and is not a prime.
    >>> largest_prime_factor(13195)
    29
    >>> largest_prime_factor(2048)
    2
    """
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    largest = 1
    i = 2
    while i <= n // i:
        if n % i == 0:
            if is_prime(n // i):
                return n // i
            if is_prime(i):
                largest = i
        i += 1
    return largest