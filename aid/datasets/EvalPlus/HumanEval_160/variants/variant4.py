def do_algebra(operator, operand):
    l_operand = len(operand)
    l_operator = len(operator)
    s = ''
    for i in range(l_operand):
        s += str(operand[i])
        if i < l_operator:
            s += operator[i]
    return eval(s)