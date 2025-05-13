from typing import List, Tuple


def sum_product(numbers: List[int]) -> Tuple[int, int]:

    s, p = 0, 1
    for number in numbers:
        s += number
        p *= number
    return s, p

