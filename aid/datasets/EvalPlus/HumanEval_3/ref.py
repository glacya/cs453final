from typing import List


def below_zero(operations: List[int]) -> bool:

    account = 0
    for operation in operations:
        account += operation
        if account < 0:
            return True
    return False

