def odd_count(lst):
    return [f"the number of odd elements {sum(int(digit) % 2 != 0 for digit in lst[i])} in the string {i+1} of the input." for i in range(len(lst))]