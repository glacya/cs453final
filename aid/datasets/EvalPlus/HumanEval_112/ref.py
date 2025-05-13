
def reverse_delete(s,c):

    ss = "".join(filter(lambda ch: ch not in c, s))
    return ss, ss == ss[::-1]

