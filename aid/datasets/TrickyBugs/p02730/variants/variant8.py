s = input()
first_half_palindrome = s[:len(s)//2]
second_half_palindrome = s[(len(s)+1)//2:]
is_strong_palindrome = s == s[::-1] and first_half_palindrome == first_half_palindrome[::-1] and second_half_palindrome == second_half_palindrome[::-1]

if is_strong_palindrome:
    print("Yes")
else:
    print("No")
