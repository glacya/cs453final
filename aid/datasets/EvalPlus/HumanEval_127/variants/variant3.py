def intersection(interval1, interval2):
    if interval1[0] > interval1[1] or interval2[0] > interval2[1]:
        return "NO"
    elif interval1[0] > interval2[1] or interval2[0] > interval1[1]:
        return "NO"
    else:
        start = max(interval1[0], interval2[0])
        end = min(interval1[1], interval2[1])
        if end < start:
            return  "NO"
        elif end - start <= 1:
            return "NO"
        else:
            length = end - start
            is_prime = True
            if length > 1:
                for i in range(2, int(length**0.5) + 1):
                    if length % i == 0:
                        is_prime = False
                        break
            return "YES" if is_prime and length > 1 else "NO"