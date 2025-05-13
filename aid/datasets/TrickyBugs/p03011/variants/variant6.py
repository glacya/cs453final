from typing import List

def min_flight_time(flight_times: List[int]) -> int:
    sorted_times = sorted(flight_times)
    return sorted_times[0] + sorted_times[1]


input_times = input().split()
flight_times = [int(time) for time in input_times]
result = min_flight_time(flight_times)
print(result)
