s = int(input())

if (9 < s < 1300) - (0 < s % 100 < 13) * 2 == 0:
    print('NA')
elif (9 < s < 1300) - (0 < s % 100 < 13) * 2 == 1:
    print('MMYY')
elif (9 < s < 1300) - (0 < s % 100 < 13) * 2 == -1:
    print('YYMM')
else:
    print('AMBIGUOUS')
