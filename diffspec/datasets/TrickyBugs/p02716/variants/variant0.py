def find_max(a):
    # Get the length of the array
    n = len(a)

    # If the length is 2 or 3, return the maximum element
    if n <= 3:
        return max(a)

    # Initialize a 2D array dp with size (n, 2 + n % 2) and fill it with a large negative number
    dp = [[-(1 << 64)] * (2 + n % 2) for _ in range(n)]

    # In the first row, set dp[i][i] and dp[i + 1][i] equal to a[i] for all i
    for i in range(2 + n % 2):
        dp[i][i] = a[i]
        dp[i + 1][i] = a[i]

    # Iterate from the third row to the last row
    for i in range(2, n):
        # Iterate through the columns
        for j in range(2 + n % 2):
            # Iterate through the extra space
            for extra_space in range(j + 1):
                # Calculate the current sum using the formula
                curr_sum = dp[i - (2 + extra_space)][j - extra_space] + a[i]
                # Update dp[i][j] if the current sum is greater
                if curr_sum > dp[i][j]:
                    dp[i][j] = curr_sum

    # Return the result
    return dp[-1][1 + n % 2]


def main():
    # Read the length of the array
    n = int(input())
    # Read the elements of the array
    a = list(map(int, input().split()))

    # Print the maximum possible sum of the chosen elements
    print(find_max(a))


main()
