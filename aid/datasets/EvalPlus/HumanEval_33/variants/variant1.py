def sort_third(l: list):
    l_prime = l.copy()
    l_third = []
    for i in range(len(l)):
        if i % 3 == 0:
            l_third.append(l[i])
            l_prime[i] = None
            
    l_third.sort()
    l_third_index = 0
    for j in range(len(l_prime)):
        if l_prime[j] == None:
            l_prime[j] = l_third[l_third_index]
            l_third_index += 1
    return l_prime