# get input from the user
a, b = input().split()

# concatenate the two numbers
x = int(a + b)

# check if the concatenated number is a square number
if int(x ** 0.5) ** 2 == x:
    print("Yes")
else:
    print("No")
