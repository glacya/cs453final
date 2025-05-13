def count_cookie_exchanges(a, b, c):
    e = a - b | b - c
    return len(bin(e & -e)) - 3 - (e == b & 1)

if __name__ == "__main__":
    a, b, c = map(int, input().split())
    print(count_cookie_exchanges(a, b, c))
