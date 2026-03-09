# 2291. Maximum Profit From Trading Stocks
# https://leetcode.com/problems/maximum-profit-from-trading-stocks/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n * b), space O(b)
    def maximumProfitDP(self, present: list[int], future: list[int], budget: int) -> int:
        # 空间优化版 DP
        n = len(present)
        dp = [0] * (budget + 1)
        for i in range(n):
            profit = future[i] - present[i]
            for b in range(budget, -1, -1):
                if b >= present[i] and present[i] < future[i]:
                    dp[b] = max(dp[b], dp[b - present[i]] + profit)
        return dp[budget]

    # time O(n * b), space O(n * b)
    def maximumProfitDPWithGrid(self, present: list[int], future: list[int], budget: int) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(present)
        dp = [[0] * (budget + 1) for _ in range(n + 1)]
        for i in range(n):
            profit = future[i] - present[i]
            for b in range(budget, -1, -1):
                if b < present[i] or present[i] >= future[i]:
                    dp[i + 1][b] = dp[i][b]
                else:
                    dp[i + 1][b] = max(dp[i][b], dp[i][b - present[i]] + profit)
        return dp[n][budget]

    # time O(n * b), space O(n * b)
    def maximumProfitDFSWithMemorization(
        self, present: list[int], future: list[int], budget: int
    ) -> int:
        # 记忆化搜索: 题目等价于在 n 个物品中选一些, 每个物品的重量是 present[i],
        # 价值是 future[i] - present[i], 求在总重量不超过 budget 的前提下, 能
        # 获得的最大价值。
        n = len(present)

        @cache
        def dfs(i: int, b: int) -> int:
            if i == -1:
                return 0
            # 如果当前物品的重量超过了剩余预算, 或者当前物品没有利润, 那么只能不选这
            # 个物品
            if b < present[i] or present[i] >= future[i]:
                return dfs(i - 1, b)
            else:  # 否则可以选择不选这个物品, 或者选这个物品
                return max(dfs(i - 1, b), dfs(i - 1, b - present[i]) + future[i] - present[i])

        return dfs(n - 1, budget)
