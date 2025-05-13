from typing import List, Tuple
def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of integers, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """
    if not numbers:
        return []
    max_so_far = numbers[0]  # Updated initial max_so_far to be the first element of the list
    result = [max_so_far]  # Initialize result with the first element itself
    for n in numbers[1:]:  # Start from the second element
        if n > max_so_far:
            max_so_far = n
        result.append(max_so_far)
    return result