def search(lst):
    if lst == []:
        return -1
    lst.sort()
    freq = [0] * (max(lst) + 1)
    for x in lst:
        freq[x] += 1
    for i in range(len(freq)-1, -1, -1):
        if i == 0:
            continue
        if freq[i] >= i and freq[i] > freq[i-1]:
            return i
    return -1