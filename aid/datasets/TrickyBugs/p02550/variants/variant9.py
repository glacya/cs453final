**REPAIRED CODE**:

n,x,m = map(int,input().split())
ans = 0
al = set([x])
for i in range(n):
  ans += x
  x = (x**2)%m
  if x==0:
    break
  if x in al:
    ind = list(al).index(x)
    loop = i-ind+1
    l = list(al)
    ans += sum(l[ind:i+1])*(((n-i-1)//loop) if (n-i-1)//loop>0 else 1)
    for j in range((n-i-1)%loop):
      ans += l[ind+j]
    break
  al.add(x)
print(ans)