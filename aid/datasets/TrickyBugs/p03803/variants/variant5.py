A,B=map(int,input().split())
if A==B: 
    print('Draw')
else: 
    if A==1 and B==13:
        print('Alice')
    elif A!=1 and B==1:
        print('Bob')
    elif A>B:
        print('Alice')
    else:
        print('Bob')
