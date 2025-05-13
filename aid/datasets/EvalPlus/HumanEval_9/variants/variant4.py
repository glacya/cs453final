from typing import List, Tuple
def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of integers, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
    max_so_far = float('-inf')  # Initialize max_so_far to negative infinity
    result = []
    for n in numbers:
        max_so_far = max(max_so_far, n)  # Update max_so_far to the maximum of current element and max_so_far
        result.append(max_so_far)
    return result