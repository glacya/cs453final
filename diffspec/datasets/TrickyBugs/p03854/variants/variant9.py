import re

def main():
    S = input()
    if re.match('(dreame*|erase|r)*$', S):
        print('YES')
    else:
        print('NO')

if __name__ == '__main__':
    main()
