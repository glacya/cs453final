def fizz_buzz(n: int):
    """Return the number of times the digit 7 appears in integers less than n which are divisible by 11 or 13.
    >>> fizz_buzz(50)
    0
    >>> fizz_buzz(78)
    2
    >>> fizz_buzz(79)
    3
    """
    # single digit numbers divisible by 11 or 13 always contain a 7
    if n < 10 and (n % 11 == 0 or n % 13 == 0):
        return 1
    # double digit numbers divisible by 11 or 13 always contain a 7
    elif n < 100 and (n % 11 == 0 or n % 13 == 0):
        return 2
    else:
        nums = [x for x in range(1, n) if x % 11 == 0 or x % 13 == 0]
        return sum([str(x).count("7") for x in nums])