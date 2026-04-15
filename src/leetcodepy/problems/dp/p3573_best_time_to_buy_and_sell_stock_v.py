# 3573. Best Time to Buy and Sell Stock V
# https://leetcode.com/problems/best-time-to-buy-and-sell-stock-v/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n * k), space O(k)
    def maximumProfitDPWithRollingArray(self, prices: list[int], k: int) -> int:
        # 状态机 DP, 滚动数组. 最多 k 轮交易, 支持做多和做空.
        # 在 p0188 (仅做多) 基础上增加做空状态, 3 个状态:
        #   h=0 (空闲): 无持仓
        #   h=1 (做多): 持有多头, 等待卖出获利
        #   h=2 (做空): 持有空头, 等待买回获利
        #
        #                  ┌──┐
        #                  ▼  │ 不操作
        #   做多 -p    ┌──────┐
        #   ┌─────────▶│ long ├─────────┐
        #   │ (消耗额度)└──────┘ 平多 +p  │
        #   │                           ▼
        #   ├──────────┌──────┐◀────────┤
        #   │    不操作 │ idle │ 不操作   │
        #   ├─────────▶└──────┘◀────────┤
        #   │                           │
        #   │ (消耗额度)┌──────┐ 平空 -p  │
        #   └─────────▶│short ├─────────┘
        #   做空 +p    └──────┘
        #                  ▲  │ 不操作
        #                  └──┘
        #
        # 开仓 (做多/做空) 消耗一轮交易额度 (j → j+1), 平仓不消耗.
        n = len(prices)
        pre = [[0, -inf, -inf] for _ in range(k + 1)]
        for i in range(n):
            dp = [[0, 0, 0]] + [[-inf, -inf, -inf] for _ in range(k)]
            for j in range(k):
                dp[j + 1][0] = max(
                    pre[j + 1][0],  # 不操作
                    pre[j + 1][2] - prices[i],  # 平空 (买回)
                    pre[j + 1][1] + prices[i],  # 平多 (卖出)
                )
                # 做多: 继续持有 or 开多仓 (消耗额度, 从第 j 笔 idle 转移)
                dp[j + 1][1] = max(pre[j + 1][1], pre[j][0] - prices[i])
                # 做空: 继续持有 or 开空仓 (消耗额度, 从第 j 笔 idle 转移)
                dp[j + 1][2] = max(pre[j + 1][2], pre[j][0] + prices[i])
            pre = dp
        return pre[k][0]

    # time O(n * k), space O(n * k)
    def maximumProfitDPWithGrid(self, prices: list[int], k: int) -> int:
        # 三维 DP, 显式保存每天状态, 便于理解.
        # dp[i+1][j+1][h]: 第 i 天, 用了 j+1 轮交易额度, 状态 h 的最大利润.
        n = len(prices)
        dp = [[[-inf, -inf, -inf] for _ in range(k + 1)] for _ in range(n + 1)]
        for j in range(k + 1):
            dp[0][j] = [0, -inf, -inf]  # 初始: 持仓不合法
        for i in range(n):
            dp[i + 1][0] = [0, 0, 0]
            for j in range(k):
                dp[i + 1][j + 1][0] = max(
                    dp[i][j + 1][0],  # 不操作
                    dp[i][j + 1][2] - prices[i],  # 平空
                    dp[i][j + 1][1] + prices[i],  # 平多
                )
                # 做多: 继续持有 or 开多仓
                dp[i + 1][j + 1][1] = max(dp[i][j + 1][1], dp[i][j][0] - prices[i])
                # 做空: 继续持有 or 开空仓
                dp[i + 1][j + 1][2] = max(dp[i][j + 1][2], dp[i][j][0] + prices[i])
        return dp[n][k][0]

    # time O(n * k), space O(n * k)
    def maximumProfitDFSWithMemorization(self, prices: list[int], k: int) -> int:
        # 记忆化搜索 (自顶向下), 与三维 DP 等价.
        # dfs(i, j, h): prices[0..i], 还剩 j+1 轮交易额度, 状态 h.
        #   h=0 空闲, h=1 做多, h=2 做空.
        n = len(prices)

        @cache
        def dfs(i: int, j: int, h: int) -> int:
            if i < 0:
                return -inf if h == 1 else 0  # 做多持仓不合法
            if j == -1:
                return 0  # 交易额度用完
            if h == 1:
                # 做多: 继续持有 or 开多仓 (消耗额度, j-1)
                return max(dfs(i - 1, j, 1), dfs(i - 1, j - 1, 0) - prices[i])
            if h == 2:
                # 做空: 继续持有 or 开空仓 (消耗额度, j-1)
                return max(dfs(i - 1, j, 2), dfs(i - 1, j - 1, 0) + prices[i])
            # 空闲: 不操作 or 平空 (买回) or 平多 (卖出)
            return max(
                dfs(i - 1, j, 0),
                dfs(i - 1, j, 2) - prices[i],
                dfs(i - 1, j, 1) + prices[i],
            )

        return dfs(n - 1, k - 1, 0)
