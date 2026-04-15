# 188. Best Time to Buy and Sell Stock IV
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(n * k), space O(k)
    def maxProfitDP(self, k: int, prices: list[int]) -> int:
        # 状态机 DP. 最多 k 笔交易, 求最大利润.
        # 在 p0122 (不限次数) 基础上增加交易次数维度 j.
        # dp[j+1][0]: 用了 j+1 笔交易额度, 不持股的最大利润
        # dp[j+1][1]: 用了 j+1 笔交易额度, 持股的最大利润
        # 买入时消耗一笔交易额度 (j → j+1), 卖出不消耗.
        #
        #   对每个交易额度 j+1:
        #              买入 -prices[i]
        #            ┌────────────────────┐ (从第 j 笔的 cash 转移)
        #            │                    ▼
        #   ┌───┐ ┌──────┐          ┌──────┐ ┌───┐
        #   │   └▶│ cash │          │ hold │◀┘   │
        #   └────◀┘      │          │      └▶────┘
        #   不操作 └──────┘          └──────┘ 不操作
        #            ▲                    │
        #            └────────────────────┘
        #              卖出 +prices[i]
        #
        n = len(prices)
        dp = [[0, -inf] for _ in range(k + 1)]
        for i in range(n):
            dp[0] = [0, 0]  # 初始: 持股不合法
            for j in range(k):
                # 持股: 继续持有 or 买入 (消耗交易额度, 从第 j 笔的 cash 转移)
                dp[j + 1][1] = max(dp[j + 1][1], dp[j][0] - prices[i])
                # 不持股: 继续空仓 or 卖出 (不消耗额度, 同笔交易内)
                dp[j + 1][0] = max(dp[j + 1][0], dp[j + 1][1] + prices[i])
        return dp[k][0]

    # time O(n * k), space O(n * k)
    def maxProfitDPWithGrid(self, k: int, prices: list[int]) -> int:
        # 三维 DP, 显式保存每天状态, 便于理解.
        # dp[i+1][j+1][0]: 第 i 天, 用了 j+1 笔交易额度, 不持股的最大利润
        # dp[i+1][j+1][1]: 第 i 天, 用了 j+1 笔交易额度, 持股的最大利润
        n = len(prices)
        dp = [[[-inf, -inf] for _ in range(k + 1)] for _ in range(n + 1)]
        for i in range(k + 1):
            dp[0][i] = [0, -inf]  # 初始: 持股不合法
        for i in range(n):
            dp[i + 1][0] = [0, 0]
            for j in range(k):
                # 持股: 继续持有 or 买入 (从第 j 笔的 cash 转移, 消耗额度)
                dp[i + 1][j + 1][1] = max(dp[i][j + 1][1], dp[i][j][0] - prices[i])
                # 不持股: 继续空仓 or 卖出
                dp[i + 1][j + 1][0] = max(dp[i][j + 1][0], dp[i][j + 1][1] + prices[i])
        return dp[n][k][0]

    # time O(n * k), space O(n * k)
    def maxProfitDFSWithMemorization(self, k: int, prices: list[int]) -> int:
        # 记忆化搜索 (自顶向下), 与三维 DP 等价.
        # dfs(i, j, h): 考虑 prices[0..i], 还剩 j+1 笔交易额度, 是否持股.
        n = len(prices)

        @cache
        def dfs(i: int, j: int, h: bool) -> int:
            if i == -1:
                return -inf if h else 0  # 未开始: 持股不合法
            if j == -1:
                return 0  # 交易额度用完, 无法再操作
            if h:
                # 持股: 继续持有 or 买入 (消耗一笔额度, j-1)
                return max(dfs(i - 1, j, True), dfs(i - 1, j - 1, False) - prices[i])
            # 不持股: 继续空仓 or 卖出 (不消耗额度)
            return max(dfs(i - 1, j, False), dfs(i - 1, j, True) + prices[i])

        return dfs(n - 1, k - 1, False)
