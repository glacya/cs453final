

def greatest_common_divisor(a: int, b: int) -> int:


    def query_gcd(a: int, b: int) -> int:
        return a if b == 0 else query_gcd(b, a % b)
    return query_gcd(a, b)    

