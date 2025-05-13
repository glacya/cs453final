def prime_fib(n: int):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    def fibonacci(n):
        if n < 0:
            return "Incorrect input"
        elif n == 0:
            return 0
        elif n == 1 or n == 2:
            return 1
        else:
            a, b = 1, 1
            for i in range(2, n):
                a, b = b, a + b
            return b
    count = 0
    i = 1
    while count < n:
        fib = fibonacci(i)
        if is_prime(fib):
            count += 1
        i += 1
    return fibonacci(i - 1)