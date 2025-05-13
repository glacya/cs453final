from typing import List, Tuple
def sum_product(numbers: List[int]) -> Tuple[int, int]:
    if not numbers:
        return (0, 1)
        
    sum_result, product_result = sum_product(numbers[1:])
    
    return (numbers[0] + sum_result, numbers[0] * product_result)