s = int(input())
if (9 < s < 1300) and (0 < s % 100 < 13):
    print('AMBIGUOUS')
elif 9 < s < 1300:
    print('YYMM')
elif 0 < s % 100 < 13:
    print('MMYY')
else:
    print('NA')
