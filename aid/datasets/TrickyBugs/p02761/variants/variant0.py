n,m=map(int,input().split())
f=sorted([list(map(int,input().split())) for i in range(m)])
if n==1:
  print(f[0][1] if m==1 else -1 if m>=2 else 0)
else:
  for i in range(10**(n-1),10**n):
    d=str(i)
    flag=True
    for b,v in f:
      if int(d[b-1])!=v:
        flag=False
        break
    if flag==True:
      print(i)
      exit()
  else:print(-1)