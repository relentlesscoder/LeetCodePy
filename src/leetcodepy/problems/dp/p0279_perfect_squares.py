# 279. Perfect Squares
# https://leetcode.com/problems/perfect-squares/
# Difficulty: Medium

from functools import cache
from math import inf, isqrt


class Solution:
    # time O(n * sqrt(n)), space O(n)
    def numSquares(self, n: int) -> int:
        # 空间优化版 DP
        m = isqrt(n)
        dp = [0] + [inf] * (n)
        for i in range(m):
            p = (i + 1) * (i + 1)
            for x in range(1, n + 1):
                if x >= p:
                    dp[x] = min(dp[x], dp[x - p] + 1)
        return dp[n]

    # time O(n * sqrt(n)), space O(n * sqrt(n))
    def numSquaresDPWithGrid(self, n: int) -> int:
        # 将记忆化搜索翻译成 DP
        m = isqrt(n)
        dp = [[0] + [inf] * (n) for _ in range(m + 1)]
        for i in range(m):
            p = (i + 1) * (i + 1)
            for x in range(1, n + 1):
                if x < p:
                    dp[i + 1][x] = dp[i][x]
                else:
                    dp[i + 1][x] = min(dp[i][x], dp[i + 1][x - p] + 1)
        return dp[m][n]

    # time O(n * sqrt(n)), space O(n * sqrt(n))
    def numSquaresDFSWithMemorization(self, n: int) -> int:
        m = isqrt(n)

        @cache
        def dfs(x: int, i: int) -> int:
            if x == 0:  # 如果剩余金额为 0, 说明之前选的完全平方数的和正好等于 n, 这是一种合法的方案
                return 0
            if i == 0:  # 如果没有完全平方数了, 说明之前选的完全平方数的和不是一种合法的方案
                return inf
            p = i * i
            if x < p:  # 如果当前完全平方数的值超过了剩余金额, 那么只能不选这个完全平方数
                return dfs(x, i - 1)
            else:  # 否则可以选择不选这个完全平方数, 或者选这个完全平方数
                return min(dfs(x, i - 1), 1 + dfs(x - p, i))

        return dfs(n, m)
