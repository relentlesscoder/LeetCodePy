# 879. Profitable Schemes
# https://leetcode.com/problems/profitable-schemes/
# Difficulty: Hard

from functools import cache


class Solution:
    # time O(n * m * p), space O(n * p)
    def profitableSchemesDP(
        self, n: int, minProfit: int, group: list[int], profit: list[int]
    ) -> int:
        # 空间优化版 DP
        mod = 10**9 + 7
        m = len(group)
        dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
        dp[0][0] = 1
        for i in range(m):
            for j in range(n, -1, -1):
                for k in range(minProfit, -1, -1):
                    if j >= group[i]:
                        dp[j][k] = (dp[j - group[i]][max(0, k - profit[i])] + dp[j][k]) % mod
        res = 0
        # 注意需要把人数维度的结果累加起来因为人数不一定要用完
        for i in range(n + 1):
            res = (res + dp[i][minProfit]) % mod
        return res

    # time O(n * m * p), space O(n * m * p)
    def profitableSchemesDPWithGrid(
        self, n: int, minProfit: int, group: list[int], profit: list[int]
    ) -> int:
        # 将记忆化搜索翻译成 DP
        mod = 10**9 + 7
        m = len(group)
        dp = [[[0] * (minProfit + 1) for _ in range(n + 1)] for _ in range(m + 1)]
        dp[0][0][0] = 1
        for i in range(m):
            for j in range(n, -1, -1):
                for k in range(minProfit, -1, -1):
                    if j >= group[i]:
                        dp[i + 1][j][k] = (
                            dp[i][j - group[i]][max(0, k - profit[i])] + dp[i][j][k]
                        ) % mod
                    else:
                        dp[i + 1][j][k] = dp[i][j][k]
        res = 0
        # 注意需要把人数维度的结果累加起来因为人数不一定要用完
        for i in range(n + 1):
            res = (res + dp[m][i][minProfit]) % mod
        return res

    # time O(n * m * p), space O(n * m * p)
    def profitableSchemesDFSWithMemorization(
        self, n: int, minProfit: int, group: list[int], profit: list[int]
    ) -> int:
        # 记忆化搜索
        mod = 10**9 + 7
        m = len(group)
        # 优化1: 将数组按照所需人数排序以便于剪枝
        t = sorted([[group[i], profit[i]] for i in range(m)])

        @cache
        def dfs(i: int, g: int, p: int) -> int:
            # 搜索终止条件:
            #   1. 数组已经遍历完
            #   2. 所剩人数小于当前任务所需人数，因为数组是排序的后面的任务都不可能完成。
            if i == m or g < t[i][0]:
                return 1 if p == 0 else 0
            # 优化2: 将最小利润限制在 0 以减少分支
            return (dfs(i + 1, g - t[i][0], max(0, p - t[i][1])) + dfs(i + 1, g, p)) % mod

        return dfs(0, n, minProfit)
