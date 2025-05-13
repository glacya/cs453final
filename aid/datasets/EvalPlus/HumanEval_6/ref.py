from typing import List


def parse_nested_parens(paren_string: str) -> List[int]:

    
    def count_depth(s: str) -> int:
        max_depth, cnt = 0, 0
        for ch in s:
            if ch == "(": cnt += 1
            if ch == ")": cnt -= 1
            max_depth = max(max_depth, cnt)
        return max_depth
    
    return [count_depth(s) for s in paren_string.split(" ") if s != ""]

