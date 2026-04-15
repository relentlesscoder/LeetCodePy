# 121. Best Time to Buy and Sell Stock
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock/
# Difficulty: Easy


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxProfit(self, prices: list[int]) -> int:
        # 贪心: 维护前缀最小值, 每天尝试以当前价格卖出.
        # 等价于 p0188 k=1 的特化, 但无需状态机.
        res, pre_min = 0, inf
        for p in prices:
            res = max(res, p - pre_min)  # 今天卖出的利润
            pre_min = min(pre_min, p)  # 更新历史最低买入价
        return res

    # time O(n), space O(1)
    def maxProfitDP(self, prices: list[int]) -> int:
        # 状态机 DP, 滚动数组. p0188 k=1 的特例.
        # pre[j+1][0/1]: 用了 j+1 笔交易额度, 不持股/持股的最大利润.
        # k=1 所以 j 只有 0 一个值, 循环只执行一次.
        n = len(prices)
        pre = [[0, -inf] for _ in range(2)]
        for i in range(n):
            dp = [[-inf, -inf] for _ in range(2)]
            dp[0] = [0, 0]
            for j in range(1):  # k=1, 只有一笔交易
                # 不持股: 继续空仓 or 卖出
                dp[j + 1][0] = max(pre[j + 1][0], pre[j + 1][1] + prices[i])
                # 持股: 继续持有 or 买入 (消耗唯一的交易额度)
                dp[j + 1][1] = max(pre[j + 1][1], pre[j][0] - prices[i])
            pre = dp
        return pre[1][0]

    # time O(n), space O(n)
    def maxProfitDPWithGrid(self, prices: list[int]) -> int:
        # 三维 DP, 显式保存每天状态. p0188 k=1 的特例.
        # dp[i+1][j+1][0/1]: 第 i 天, 用了 j+1 笔交易额度, 不持股/持股.
        n = len(prices)
        dp = [[[-inf, -inf] for _ in range(2)] for _ in range(n + 1)]
        for j in range(2):
            dp[0][j] = [0, -inf]  # 初始: 持股不合法
        for i in range(n):
            dp[i + 1][0] = [0, 0]
            for j in range(1):  # k=1
                dp[i + 1][j + 1][0] = max(dp[i][j + 1][0], dp[i][j + 1][1] + prices[i])
                dp[i + 1][j + 1][1] = max(dp[i][j + 1][1], dp[i][j][0] - prices[i])
        return dp[n][1][0]

    # time O(n), space O(n)
    def maxProfitDFSWithMemorization(self, prices: list[int]) -> int:
        # 记忆化搜索 (自顶向下). p0188 k=1 的特例.
        # dfs(i, j, hold): prices[0..i], 还剩 j+1 笔交易额度, 是否持股.
        # k=1, 所以入口 j=0, 买入后 j 变为 -1 (额度用完).
        n = len(prices)

        @cache
        def dfs(i: int, j: int, hold: bool) -> int:
            if i == -1:
                return -inf if hold else 0
            if j == -1:
                return 0  # 交易额度用完, 无法再操作
            if hold:
                # 持股: 继续持有 or 买入 (消耗额度, j-1)
                return max(dfs(i - 1, j, True), dfs(i - 1, j - 1, False) - prices[i])
            # 不持股: 继续空仓 or 卖出
            return max(dfs(i - 1, j, False), dfs(i - 1, j, True) + prices[i])

        return dfs(n - 1, 0, False)
