#!/usr/bin/env python
# coding: utf-8

def ri():
    return int(input())

def rl():
    return list(input().split())

def rli():
    return list(map(int, input().split()))

def main():
    n, k = rli()
    la = rli()
    MOD = len(la)
    lb = [-1 for _ in range(len(la))]
    periods = dict()
    for i, a in enumerate(la):
        periods.setdefault(a, [])
        periods[a].append(i)
    for v in periods.values():
        for i, e in enumerate(v):
            if i == len(v)-1:
                lb[e] = (v[0] + 1) % MOD
            else:
                lb[e] = (v[i+1] + 1) % MOD
    loop = [0]
    b = 0
    while True:
        nb = lb[b]
        if nb == 0:
            break
        if nb-b <= 1:
            loop.append(nb)
        b = nb
    # 周期を計算
    period = len(loop)
    if loop[-1] == len(loop)-1:
        loop.append(None)
        period += 1

    start = loop[(k-1)%period]
    if start is None:
        print()
        return
    lc = la[start:]

    counts = dict()
    for i, a in enumerate(lc):
        counts.setdefault(a, 0)
        counts[a] += 1

    ans = []
    target = None
    for a in lc:
        if target is None:
            count = counts[a]
            if counts[a] >= 2:
                target = a
            else:
                ans.append(a)
        else:
            counts[a] -= 1
            if a == target:
                counts[a] -= 1
                target = None
    # print(la[start:], lc)
    # print(lb, loop)
    if len(ans) == 0:
        print()
    else:
        print(" ".join(map(str, ans)))


if __name__ == '__main__':
    main()

