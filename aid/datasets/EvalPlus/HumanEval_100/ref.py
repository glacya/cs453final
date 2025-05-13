
def make_a_pile(n):


    ans, num = [], n
    for _ in range(n):
        ans.append(num)
        num += 2
    return ans

