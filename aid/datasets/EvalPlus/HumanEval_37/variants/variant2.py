def sort_even(l: list):
    new_list = l[:]
    even_index_ints = [i for i in new_list if new_list.index(i) % 2 == 0]
    even_index_ints.sort()
    index = 0
    for i in range(len(l)):
        if i % 2 == 0:
            new_list[i] = even_index_ints[index]
            index += 1
    return new_list