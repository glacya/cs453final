import math

def max_fill(grid, capacity):


    ans = 0    
    for l in grid:
        ans += math.ceil(sum(l) / capacity)
    return ans

