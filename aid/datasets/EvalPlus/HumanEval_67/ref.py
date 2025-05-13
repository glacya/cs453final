
def fruit_distribution(s,n):


    words = s.split(" ")
    c1, c2 = int(words[0]), int(words[3])
    assert n - c1 - c2 >= 0, "invalid inputs" # $_CONTRACT_$
    
    return n - c1 - c2

