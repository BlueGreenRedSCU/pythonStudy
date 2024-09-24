#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2023/3/3 12:01 PM
# @Author : ritong.lan
# @File : leetcode.py

import pytest
import bisect
from collections import deque


@pytest.mark.parametrize("names", [(["pes","fifa","gta","pes(2019)"]),
                                   (["gta","gta(1)","gta","avalon"])])
def test_lc_1487(names):
    """
    用字典d记录当前前缀序号的最大值，遍历names
    如果name不在d中，直接append进ans，并且设置d[name]=1，意思是name的序号最大值为1
    如果name在d中，则从i=d[name]开始，判断name+i组成的文件名是否在d中，如果在就继续遍历，不在就退出，把当前序号加给文件名，append进入ans，然后让d[name]=i，这样可以减少下次遍历的时间
    """
    ans = []
    d = dict()
    for name in names:
        if name in d:
            i = d[name]
            while "{}({})".format(name, i) in d:
                i += 1
            ans.append("{}({})".format(name, i))
            d["{}({})".format(name, i)] = 1
            d[name] = i + 1
        else:
            ans.append(name)
            d[name] = 1
    print(ans)
    return ans



@pytest.mark.parametrize("nums, p", [([3,1,4,2], 6),
                                     ([6,3,5,2], 9),
                                     ([1,2,3], 3),
                                     ([1,2,3], 7)])
def test_lc_1590(nums, p):
    """
    定理1：if y % p = x, then (y - z) % p = 0 -> z % p == x
    定理2: (y - z) % p = x -> z % p = (y - x) mod p
    (a + b) % p = (a % p + b % p) % p
    """
    # total = sum(nums)
    # if total % p == 0:
    #     return 0
    # index = {0: -1}
    # ans = len(nums)
    # cur = 0
    # for i, n in enumerate(nums):
    #     cur = (cur + n) % p
    #     if (cur-total) % p in index:
    #         ans = min(ans, i - index[(cur-total) % p])
    #     index[cur] = i
    # print(ans)
    # return ans if ans < len(nums) else 1

    total = sum(nums)
    index = {0: -1}
    cur = 0
    ans = len(nums)
    for i, n in enumerate(nums):
        cur = (cur + n) % p
        print((cur - total) % p)
        if (cur - total) % p in index:
            ans = min(ans, i - index[(cur - total) % p])
        index[cur] = i
    print(ans)


def test_lc_1615(n, roads):
    """
    先直接创建邻接表，然后双重循环遍历这个邻接表
    因为是双向道路，所以邻接表中某点的set的长度就是和该点连接的点数
    然后加一个特殊判断，如果当前遍历的两个点相连，就让秩-=1
    在过程中更新ans即可
    """
    t = [set() for _ in range(n)]
    for x, y in roads:
        t[x].add(y)
        t[y].add(x)
    ans = 0
    for x in range(n):
        for y in range(x+1, n):
            cur = len(t[x]) + len(t[y])
            if x in t[y]:
                cur -= 1
            ans = max(ans, cur)
    return ans


def test_lc_2389(nums, queries):
    ans = []
    for n in queries:
        newnums = nums[:]
        newnums.sort()
        total = sum(newnums)
        while newnums and total > n:
            total -= newnums.pop()
        ans.append(len(newnums))
    return ans


@pytest.mark.parametrize("scores, ages", [([4,5,6,5], [2,1,2,1])])
def test_lc_1626(scores, ages):
    age_score = []
    for a, s in zip(ages, scores):
        age_score.append([a, s])
    age_score.sort(key = lambda x: (x[0], x[1]))


@pytest.mark.parametrize("n", [1,2,33])
def test_lc_1641(n):
    ans = [1 for _ in range(5)]
    for i in range(n):
        temp = [0 for _ in range(5)]
        for j in range(5):
            temp[j] = sum(temp[j+1:])
        ans = temp
    return sum(ans)


@pytest.mark.parametrize("forbbiden, a, b, x", [([14,4,18,1,15], 3, 15, 9)])
def test_lc_1654(forbbiden, a, b, x):
    return 0


@pytest.mark.parametrize("ranks, cars", [([4,2,3,1], 10),
                                         ([5,1,8], 6)])
def test_lc_2594(ranks, cars):
    def check(time):
        ret = 0
        for n in ranks:
            ret += int((time/n)**0.5)
        return ret

    l, r = 0, max(ranks) * cars * cars
    print(l, r)
    while l < r:
        print(l, r)
        time = (l + r) // 2
        if check(time) < cars:
            l = time + 1
        else:
            r = time
    print(l)


@pytest.mark.parametrize("spells, potions, success", [([5,1,3], [1,2,3,4,5],7),
                                                      ([3,1,2], [8,5,8],16)])
def test_lc_2300(spells, potions, success):
    potions.sort()
    ans = []
    for n in spells:
        ans.append(len(potions) - bisect.bisect_left(potions, success/n))
    print(ans)


def reverseOddLevels(self, root):
    q = deque([root])
    q2 = deque([])
    layer = 0
    while q:
        layer += 1
        while q:
            cur_root = q.popleft()
            if cur_root.left:
                q2.append(cur_root.left)
                q2.append(cur_root.right)
        if not q2:
            break
        if layer % 2:
            for i in range(len(q2)//2):
                q2[i].val, q2[len(q2) - 1 - i].val = q2[len(q2) - 1 - i].val, q2[i].val
        q, q2 = q2, deque([])
    return root


def findPeakElement(self, nums) -> int:
    nums = [float('-inf')] + nums + [float('-inf')]
    for i in range(1, len(nums)-1):
        if nums[i] > nums[i-1] and nums[i] > nums[i+1]:
            return i-1


# if __name__ == "__main__":
    # print(lc_1487())
    # print(lc_1487())
    # print(lc_1487(["onepiece","onepiece(1)","onepiece(2)","onepiece(3)","onepiece"]))
    # print(lc_1487(["wano","wano","wano","wano"]))
    # print(lc_1487(["kaido","kaido(1)","kaido","kaido(1)"]))




































