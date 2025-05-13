def largest_prime_factor(n: int):
    largest = 1
    # Starting with the smallest prime 2.
    i = 2
    while i <= n / i:  # Loop until the square root of n
        if n % i == 0:
            largest = i
            n = n // i
        else:
            i += 1
    if n > largest:  # If n is greater than sqrt(n), then it is a prime.
        largest = n
    return largest