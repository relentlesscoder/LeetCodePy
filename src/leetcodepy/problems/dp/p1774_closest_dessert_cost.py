# 1774. Closest Dessert Cost
# https://leetcode.com/problems/closest-dessert-cost/
# Difficulty: Medium

from functools import cache
from math import inf
from itertools import pairwise

class Solution:

    # time O(n * m * t), space O(m * t)
    def closestCostDFSWithMemorization(self, baseCosts: list[int], toppingCosts: list[int], target: int) -> int:

        # 比较绝对值
        def compare(a: int, b: int) -> int:
            if abs(a) == abs(b):
                return max(a, b)
            elif abs(a) < abs(b):
                return a
            else:
                return b

        @cache
        def dfs(i: int, c: int) -> int:
            if i < 0: # 数组已遍历完返回当前的差值
                return c
            x = toppingCosts[i]
            if c == x: # 差值达到 0
                return 0
            elif c < x: # 如果差值小于当前配料的价格
                # 选 - 注意如果选当前的配料则差值会变负，立即返回因为继续处理
                # 只能使这个差值的绝对值更大
                s1 = c - x 
                s2 = dfs(i - 1, c) # 不选
                return compare(s1, s2)
            else:
                s1 = dfs(i - 1, c) # 不选
                s2 = dfs(i - 1, c - x) # 选一个
                s3 = dfs(i - 1, c - 2 * x) # 选两个
                # 找到绝对值最小的差值
                r2 = inf
                for a, b in pairwise([s1, s2, s3, s1]):
                    r1 = compare(a, b)
                    r2 = compare(r1, r2)
                return r2

        res = inf
        m = len(toppingCosts)
        unique = list(set(baseCosts)) # 优化: 去重 
        for x in unique:
            ans = dfs(m - 1, target - x) # 计算与 target 绝对值最小的差值
            res = compare(res, ans)
        return target - res
