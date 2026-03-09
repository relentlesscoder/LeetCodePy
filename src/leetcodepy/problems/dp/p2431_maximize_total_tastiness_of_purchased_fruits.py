# 2431. Maximize Total Tastiness of Purchased Fruits
# https://leetcode.com/problems/maximize-total-tastiness-of-purchased-fruits/
# Difficulty: Medium

from functools import cache


class Solution:
    # time O(n * c * a), space O(c * a)
    def maxTastiness(
        self, price: list[int], tastiness: list[int], maxAmount: int, maxCoupons: int
    ) -> int:
        # 空间优化版 DP
        n = len(price)
        dp = [[0] * (maxAmount + 1) for _ in range(maxCoupons + 1)]
        for i in range(n):
            p = price[i]
            h = p // 2
            t = tastiness[i]
            for c in range(maxCoupons, -1, -1):
                for a in range(maxAmount, -1, -1):
                    if a >= p:
                        dp[c][a] = max(dp[c][a], dp[c][a - p] + t)
                    if c > 0 and a >= h:
                        dp[c][a] = max(dp[c][a], dp[c - 1][a - h] + t)
        return dp[maxCoupons][maxAmount]

    # time O(n * c * a), space O(n * c * a)
    def maxTastinessDPWithGrid(
        self, price: list[int], tastiness: list[int], maxAmount: int, maxCoupons: int
    ) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(price)
        dp = [[[0] * (maxAmount + 1) for _ in range(maxCoupons + 1)] for _ in range(n + 1)]
        for i in range(n):
            p = price[i]
            h = p // 2
            t = tastiness[i]
            for c in range(maxCoupons, -1, -1):
                for a in range(maxAmount, -1, -1):
                    dp[i + 1][c][a] = dp[i][c][a]
                    if a >= p:
                        dp[i + 1][c][a] = max(dp[i + 1][c][a], dp[i][c][a - p] + t)
                    if c > 0 and a >= h:
                        dp[i + 1][c][a] = max(dp[i + 1][c][a], dp[i][c - 1][a - h] + t)
        return dp[n][maxCoupons][maxAmount]

    # time O(n * c * a), space O(n * c * a)
    def maxTastinessDFSWithMemorization(
        self, price: list[int], tastiness: list[int], maxAmount: int, maxCoupons: int
    ) -> int:
        # 记忆化搜索: 题目等价于在 n 个物品中选一些, 每个物品有三种状态: 不选, 用优惠券买, 或者直接买。
        n = len(price)

        @cache
        def dfs(i: int, c: int, a: int) -> int:
            if i == -1:
                return 0
            p = price[i]  # 原价格
            h = p // 2  # 用优惠券买的价格
            t = tastiness[i]  # 美味程度
            res = dfs(i - 1, c, a)  # 不选这个物品
            if a >= p:  # 直接买这个物品
                res = max(res, dfs(i - 1, c, a - p) + t)
            if c > 0 and a >= h:  # 用优惠券买这个物品
                res = max(res, dfs(i - 1, c - 1, a - h) + t)
            return res

        return dfs(n - 1, maxCoupons, maxAmount)
