import math
def minSubArraySum(nums):
    """
    Given an array of integers nums, find the minimum sum of any non-empty sub-array
    of nums.
    Example
    minSubArraySum([2, 3, 4, 1, 2, 4]) == 1
    minSubArraySum([-1, -2, -3]) == -6
    """
    if len(nums) == 1:
        return nums[0]
    elif len(nums) == 2:
        return min(nums[0], nums[1])
    else:
        min_sum = math.inf
        total_sum = 0
        for num in nums:
            total_sum += num
            min_sum = min(min_sum, total_sum)
            total_sum = max(total_sum, 0)  # Reset total_sum to 0 if it becomes negative
        return min_sum