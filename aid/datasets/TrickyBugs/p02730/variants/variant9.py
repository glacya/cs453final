s = input()

# check if the string is a palindrome
if s != s[::-1]:
    print("No")
else:
    n = len(s)
    # check if the first half of the string is a palindrome
    if s[:n//2] != s[:n//2][::-1]:
        print("No")
    # check if the second half of the string is a palindrome
    elif s[(n+1)//2:] != s[(n+1)//2:][::-1]:
        print("No")
    else:
        print("Yes")
