
def solve(N):


    s = sum(map(lambda x: int(x), str(N)))
    return bin(s)[2:]

