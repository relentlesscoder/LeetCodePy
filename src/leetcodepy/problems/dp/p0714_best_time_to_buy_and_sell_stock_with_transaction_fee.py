# 714. Best Time to Buy and Sell Stock with Transaction Fee
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxProfitDP(self, prices: list[int], fee: int) -> int:
        # 状态机 DP, 滚动变量. 与 p0122 相同但每笔交易需付手续费.
        # 手续费在买入时扣除 (也可在卖出时扣, 效果相同).
        #
        #         买入 -(prices[i] + fee)
        #            ┌────────────────────┐
        #            │                    ▼
        #   ┌───┐ ┌──────┐          ┌──────┐ ┌───┐
        #   │   └▶│  p0  │          │  p1  │◀┘   │
        #   └────◀┘      │          │      └▶────┘
        #   不操作 └──────┘          └──────┘ 不操作
        #            ▲                    │
        #            └────────────────────┘
        #              卖出 +prices[i]
        #
        # p0: 不持股的最大利润, p1: 持股的最大利润
        n, p0, p1 = len(prices), 0, -inf
        for i in range(n):
            temp = p0  # 暂存旧 p0, 防止买入时用到已更新的 p0
            p0 = max(p0, p1 + prices[i])  # 卖出或不动
            p1 = max(p1, temp - prices[i] - fee)  # 买入(含手续费)或不动
        return p0

    # time O(n), space O(n)
    def maxProfitDPWithGrid(self, prices: list[int], fee: int) -> int:
        # 数组 DP, 显式保存每天状态, 便于理解.
        # dp[i+1][0]: 第 i 天结束不持股的最大利润
        # dp[i+1][1]: 第 i 天结束持股的最大利润
        # 与 p0122 唯一区别: 买入时额外扣除 fee.
        n = len(prices)
        dp = [[0, -inf]] + [[-inf, -inf] for _ in range(n)]
        for i in range(n):
            dp[i + 1][0] = max(dp[i][0], dp[i][1] + prices[i])  # 不动或卖出
            dp[i + 1][1] = max(dp[i][1], dp[i][0] - prices[i] - fee)  # 不动或买入
        return dp[n][0]

    # time O(n), space O(n)
    def maxProfitDFSWithMemorization(self, prices: list[int], fee: int) -> int:
        # 记忆化搜索 (自顶向下), 与数组 DP 等价.
        # dfs(i, h): 考虑 prices[0..i], 当前是否持股 (h=1/0), 的最大利润.
        # 与 p0122 唯一区别: 买入时额外扣除 fee.
        n = len(prices)

        @cache
        def dfs(i: int, h: int) -> int:
            if i == -1:
                return -inf if h == 1 else 0  # 未开始: 持股不合法
            if h == 1:
                # 持股: 继续持有 or 买入 (扣手续费)
                return max(dfs(i - 1, 1), dfs(i - 1, 0) - prices[i] - fee)
            # 不持股: 继续空仓 or 卖出
            return max(dfs(i - 1, 0), dfs(i - 1, 1) + prices[i])

        return dfs(n - 1, 0)
