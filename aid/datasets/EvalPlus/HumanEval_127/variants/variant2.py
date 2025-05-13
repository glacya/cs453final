def intersection(interval1, interval2):
    if interval1[0] > interval1[1] or interval2[0] > interval2[1]:
        return "NO"
    elif interval1[0] > interval2[1] or interval2[0] > interval1[1]:
        return "NO"
    else:
        start = max(interval1[0], interval2[0])
        end = min(interval1[1], interval2[1])
        
        if (end - start) <= 1:  # Corrected condition for intersection of length <= 1
            return "NO"
        else:
            is_prime = True
            for i in range(2, int((end - start) ** 0.5) + 1):
                if (end - start) % i == 0:
                    is_prime = False
                    break
            if is_prime and end - start > 1:  # Prime numbers are greater than 1
                return "YES"
            else:
                return "NO"