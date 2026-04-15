# 309. Best Time to Buy and Sell Stock with Cooldown
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxProfitDP(self, prices: list[int]) -> int:
        # 状态机 DP, 滚动变量. 与 p0122 相同但卖出后需冷却一天.
        # 买入时不能用"昨天"的 cash, 必须用"前天"的 cash (跳过冷却日).
        #
        #              买入 -prices[i]
        #            ┌────────────────────┐ (从前天的 cash 转移)
        #            │                    ▼
        #   ┌───┐ ┌──────┐          ┌──────┐ ┌───┐
        #   │   └▶│ cash │          │ hold │◀┘   │
        #   └────◀┘      │          │      └▶────┘
        #   不操作 └──────┘          └──────┘ 不操作
        #            ▲                    │
        #            └────────────────────┘
        #              卖出 +prices[i]
        #
        # cash1: 昨天不持股的最大利润 (即 dp[i][0])
        # cash0: 前天不持股的最大利润 (即 dp[i-1][0]), 用于买入时跳过冷却
        # hold:  昨天持股的最大利润
        n = len(prices)
        hold, cash0, cash1 = -inf, 0, 0
        for i in range(n):
            c = max(cash1, hold + prices[i])  # 卖出: 昨天持股转移; 不操作: 昨天不持股转移
            h = max(
                hold, (cash0 if i >= 1 else 0) - prices[i]
            )  # 买入: 前天不持股转移 (跳过冷却); 不操作: 昨天持股转移
            cash0 = cash1  # 滚动: 昨天的 cash 变成前天的 cash
            cash1 = c  # 昨天的 cash 更新为当前计算的值
            hold = h  # 昨天的 hold 更新为当前计算的值
        return cash1

    # time O(n), space O(n)
    def maxProfitDPWithArray(self, prices: list[int]) -> int:
        # 数组 DP, 显式保存每天状态, 便于理解.
        # dp[i+1][0]: 第 i 天结束不持股的最大利润
        # dp[i+1][1]: 第 i 天结束持股的最大利润
        # 与 p0122 唯一区别: 买入时引用 dp[i-1][0] (前天) 而非 dp[i][0] (昨天).
        n = len(prices)
        dp = [[0, -inf]] + [[0] * (2) for _ in range(n)]
        for i in range(n):
            dp[i + 1][0] = max(dp[i][0], dp[i][1] + prices[i])  # 不动或卖出
            # 买入: 从前天的不持股状态转移, 跳过卖出后的冷却日
            dp[i + 1][1] = max(dp[i][1], (dp[i - 1][0] if i >= 1 else 0) - prices[i])
        return dp[n][0]

    # time O(n), space O(n)
    def maxProfitDFSWithMemorization(self, prices: list[int]) -> int:
        # 记忆化搜索 (自顶向下), 与数组 DP 等价.
        # dfs(i, hold): 考虑 prices[0..i], 当前是否持股, 的最大利润.
        # 买入时递归到 i-2 (跳过冷却日), 而非 p0122 的 i-1.
        n = len(prices)

        @cache
        def dfs(i: int, hold: bool) -> int:
            if i < 0:
                return -inf if hold else 0  # 未开始: 持股不合法, 不持股利润为 0
            if hold:
                # 持股: 继续持有 or 今天买入 (从前天不持股转移, 跳过冷却)
                return max(dfs(i - 1, True), dfs(i - 2, False) - prices[i])
            # 不持股: 继续空仓 or 今天卖出
            return max(dfs(i - 1, False), dfs(i - 1, True) + prices[i])

        return dfs(n - 1, False)
