s = input().strip()
k = int(input().strip())

for i, v in enumerate(s):
  if i + 1 == k or int(v) > 1:
    print(v)
    break