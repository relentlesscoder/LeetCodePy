# 1774. Closest Dessert Cost
# https://leetcode.com/problems/closest-dessert-cost/
# Difficulty: Medium

from functools import cache
from math import inf


class Solution:
    # time O(m * t), space O(t)
    def closestCost(self, baseCosts: list[int], toppingCosts: list[int], target: int) -> int:
        # 空间优化版 DP
        res = inf
        m = len(toppingCosts)
        unique = list(set(baseCosts))

        dp = list(range(target + 1))

        for i in range(m):
            x = toppingCosts[i]
            y = 2 * toppingCosts[i]
            for c in range(target, -1, -1):
                if c <= x:
                    dp[c] = self._compare(dp[c], c - x)
                elif c <= y:
                    dp[c] = self._compare(dp[c], self._compare(dp[c - x], c - y))
                else:
                    dp[c] = self._compare(dp[c], self._compare(dp[c - x], dp[c - y]))
        for x in unique:
            res = self._compare(res, target - x if target <= x else dp[target - x])

        return target - res

    # time O(m * t), space O(m * t)
    def closestCostDPWithGrid(
        self, baseCosts: list[int], toppingCosts: list[int], target: int
    ) -> int:
        # 将记忆化搜索翻译成 DP
        res = inf
        m = len(toppingCosts)
        unique = list(set(baseCosts))

        dp = [[0] * (target + 1) for _ in range(m + 1)]
        dp[0] = list(range(target + 1))

        for i in range(m):
            x = toppingCosts[i]
            y = 2 * toppingCosts[i]
            for c in range(target, -1, -1):
                if c <= x:  # 不选或者选一个 - 选一个变成负数直接返回
                    dp[i + 1][c] = self._compare(dp[i][c], c - x)
                elif c <= y:  # 不选，选一个或者选两个 - 选两个变成负数直接返回
                    dp[i + 1][c] = self._compare(dp[i][c], self._compare(dp[i][c - x], c - y))
                else:  # 不选，选一个或者选两个
                    dp[i + 1][c] = self._compare(
                        dp[i][c], self._compare(dp[i][c - x], dp[i][c - y])
                    )
        for x in unique:
            res = self._compare(res, target - x if target <= x else dp[m][target - x])

        return target - res

    # time O(m * t), space O(m * t)
    def closestCostFSWithMemorization(
        self, baseCosts: list[int], toppingCosts: list[int], target: int
    ) -> int:
        # 记忆化搜索
        res = inf
        m = len(toppingCosts)
        unique = list(set(baseCosts))  # 优化: 去重

        @cache
        def dfs(i: int, c: int) -> int:
            # 搜索终止条件:
            #   1. 数组已经遍历完
            #   2. 当前成本已经超过目标，此时继续搜索不会得到更优解
            if i == -1 or c <= 0:
                return c
            return self._compare(
                dfs(i - 1, c),
                self._compare(dfs(i - 1, c - toppingCosts[i]), dfs(i - 1, c - 2 * toppingCosts[i])),
            )

        for x in unique:
            res = self._compare(res, dfs(m - 1, target - x))

        return target - res

    @staticmethod
    def _compare(a: int, b: int) -> int:
        x = a if a >= 0 else -a
        y = b if b >= 0 else -b
        if x == y:
            return a if a >= b else b
        elif x < y:
            return a
        else:
            return b
