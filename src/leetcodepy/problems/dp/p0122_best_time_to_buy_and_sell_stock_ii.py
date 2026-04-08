# 122. Best Time to Buy and Sell Stock II
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxProfitDP(self, prices: list[int]) -> int:
        # 状态机 DP, 滚动变量. 不限交易次数, 求最大利润.
        #
        #              买入 -prices[i]
        #            ┌────────────────────┐
        #            │                    ▼
        #   ┌───┐ ┌──────┐          ┌──────┐ ┌───┐
        #   │   └▶│ cash │          │ hold │◀┘   │
        #   └────◀┘      │          │      └▶────┘
        #   不操作 └──────┘          └──────┘ 不操作
        #            ▲                    │
        #            └────────────────────┘
        #              卖出 +prices[i]
        #
        # cash: 当前不持股的最大利润
        # hold: 当前持股的最大利润
        # 转移:
        #   cash = max(继续不持股, 卖出: hold + prices[i])
        #   hold = max(继续持股, 买入: cash - prices[i])
        # 初始: hold = -inf (未买过不可能持股), cash = 0.
        n = len(prices)
        hold, cash = -inf, 0
        for i in range(n):
            temp = cash  # 暂存旧 cash, 防止买入时用到已更新的 cash
            cash = max(cash, hold + prices[i])  # 卖出或不动
            hold = max(hold, temp - prices[i])  # 买入或不动
        return cash

    # time O(n), space O(n)
    def maxProfitDPWithArray(self, prices: list[int]) -> int:
        # 数组 DP, 显式保存每天状态, 便于理解.
        # dp[i+1][0]: 第 i 天结束不持股的最大利润
        # dp[i+1][1]: 第 i 天结束持股的最大利润
        n = len(prices)
        dp = [[0, -inf]] + [[0] * 2 for _ in range(n)]
        for i in range(n):
            dp[i + 1][0] = max(dp[i][0], dp[i][1] + prices[i])  # 不动或卖出
            dp[i + 1][1] = max(dp[i][1], dp[i][0] - prices[i])  # 不动或买入
        return dp[i + 1][0]

    # time O(n), space O(n)
    def maxProfitDFSWithMemorization(self, prices: list[int]) -> int:
        # 记忆化搜索 (自顶向下), 与数组 DP 等价.
        # dfs(i, hold): 考虑 prices[0..i], 当前是否持股, 的最大利润.
        n = len(prices)

        @cache
        def dfs(i: int, hold: bool) -> int:
            if i == -1:
                return -inf if hold else 0  # 未开始: 持股不合法, 不持股利润为 0
            if hold:
                # 持股: 继续持有 or 今天买入 (用前一天不持股的利润 - 买入价)
                return max(dfs(i - 1, True), dfs(i - 1, False) - prices[i])
            # 不持股: 继续空仓 or 今天卖出 (用前一天持股的利润 + 卖出价)
            return max(dfs(i - 1, False), dfs(i - 1, True) + prices[i])

        return dfs(n - 1, False)
