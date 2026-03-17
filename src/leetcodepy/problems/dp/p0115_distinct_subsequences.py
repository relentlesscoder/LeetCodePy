# 115. Distinct Subsequences
# https://leetcode.com/problems/distinct-subsequences/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def numDistinct(self, s: str, t: str) -> int:
        # 继续优化成一个数组
        m = len(s)
        n = len(t)
        dp = [1] + [0] * (n)
        for i in range(m):
            pre = dp[0]
            for j in range(n):
                x = dp[j + 1]
                if s[i] == t[j]:
                    dp[j + 1] += pre
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def numDistinctDPWithGrid(self, s: str, t: str) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(s)
        n = len(t)
        dp = [[1] + [0] * (n) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                dp[i + 1][j + 1] = dp[i][j + 1]
                if s[i] == t[j]:
                    dp[i + 1][j + 1] += dp[i][j]
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def numDistinctDFSWithMemorization(self, s: str, t: str) -> int:
        m = len(s)
        n = len(t)

        @cache
        def dfs(i: int, j: int) -> int:
            if j == -1:  # t 数组先空了说明 s 数组的子序列成功匹配了 t 结果加 1
                return 1
            if i == -1:  # s 数组先空了说明 s 数组的子序列无法匹配 t 结果不变
                return 0
            res = dfs(i - 1, j)  # 总是可以选择不匹配 s[i] 和 t[j]
            if s[i] == t[j]:  # 如果 s[i] 和 t[j] 相同还可以选择匹配 s[i] 和 t[j]
                res += dfs(i - 1, j - 1)
            return res

        return dfs(m - 1, n - 1)
