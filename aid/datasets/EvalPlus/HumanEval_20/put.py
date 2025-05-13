from typing import List, Tuple


def find_closest_elements(numbers: List[float]) -> Tuple[float, float]:
    """ From a supplied list of numbers (of length at least two) select and return two that are the closest to each
    other and return them in order (smaller number, larger number).
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.2])
    (2.0, 2.2)
    >>> find_closest_elements([1.0, 2.0, 3.0, 4.0, 5.0, 2.0])
    (2.0, 2.0)
    """
    if len(numbers) < 2:
        raise ValueError("List must contain at least two numbers")

    closest_numbers = sorted(numbers)
    closest_numbers_difference = abs(closest_numbers[0] - closest_numbers[1])
    closest_numbers_index = 0

    for i in range(1, len(closest_numbers)):
        if abs(closest_numbers[i] - closest_numbers[i - 1]) < closest_numbers_difference:
            closest_numbers_difference = abs(closest_numbers[i] - closest_numbers[i - 1])
            closest_numbers_index = i

    return closest_numbers[closest_numbers_index - 1], closest_numbers[closest_numbers_index]
