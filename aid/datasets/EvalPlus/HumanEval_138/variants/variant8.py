def is_equal_to_sum_even(n):
    """Evaluate whether the given number n can be written as the sum of exactly 4 positive even numbers
    Example
    is_equal_to_sum_even(4) == False
    is_equal_to_sum_even(6) == False
    is_equal_to_sum_even(8) == True
    """
    n_even = [i for i in range(2, n + 1) if i % 2 == 0]
    for i in n_even:
        for j in n_even:
            for k in n_even:
                for l in n_even:
                    if i + j + k + l == n:
                        return True
    return False