from typing import List


def rescale_to_unit(numbers: List[float]) -> List[float]:


    ma, mi = max(numbers), min(numbers)
    k = 1 / (ma - mi)
    return list(map(lambda x: (x - mi) * k, numbers))

