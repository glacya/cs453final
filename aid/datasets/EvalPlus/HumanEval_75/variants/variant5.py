def is_multiply_prime(a):
    """Write a function that returns true if the given number is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that (a) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """
    def is_prime(num):
        if num <= 1:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    if a < 100:
        for i in range(2, 100):
            if is_prime(i):
                for j in range(i, 100):
                    if is_prime(j):
                        for k in range(j, 100):
                            if is_prime(k) and i * j * k == a:
                                return True
        return False