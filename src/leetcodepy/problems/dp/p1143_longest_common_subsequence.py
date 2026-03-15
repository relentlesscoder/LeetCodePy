# 1143. Longest Common Subsequence
# https://leetcode.cn/problems/longest-common-subsequence/description/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # 继续优化成一个数组
        m = len(text1)
        n = len(text2)

        dp = [0] * (n + 1)
        for i in range(m):
            pre = dp[0]  # dp[i - 1][j - 1]
            for j in range(n):
                x = dp[j + 1]  # 在被覆盖之前先保存
                if text1[i] == text2[j]:
                    dp[j + 1] = 1 + pre
                else:
                    dp[j + 1] = max(dp[j], dp[j + 1])
                pre = x  # 更新 pre 的值为计算下一个格子需要的 dp[i - 1][j - 1]

        return dp[n]

    # time O(m * n), space O(n)
    def longestCommonSubsequenceRollingArray(self, text1: str, text2: str) -> int:
        # 空间优化版 DP
        m = len(text1)
        n = len(text2)

        dp = [0] * (n + 1)
        for i in range(m):
            next = [0] * (n + 1)
            for j in range(n):
                if text1[i] == text2[j]:
                    next[j + 1] = 1 + dp[j]
                else:
                    next[j + 1] = max(next[j], dp[j + 1])
            dp = next

        return dp[n]

    # time O(m * n), space O(m * n)
    def longestCommonSubsequenceDPWithGrid(self, text1: str, text2: str) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(text1)
        n = len(text2)

        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if text1[i] == text2[j]:
                    dp[i + 1][j + 1] = 1 + dp[i][j]
                else:
                    dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])

        return dp[m][n]

    # time O(m * n), space O(m * n)
    def longestCommonSubsequenceDFSWithMemorization(self, text1: str, text2: str) -> int:
        # 记忆化搜索
        m = len(text1)
        n = len(text2)

        @cache
        def dfs(i: int, j: int) -> int:
            if i < 0 or j < 0:  # 两个字符串至少有一个已经被完全匹配了
                return 0
            # 如果两个字符串的最后一个字符相同，那么最长公共子序列的长度就是两个字符串去掉最后一个字符之后
            # 的最长公共子序列的长度加 1
            if text1[i] == text2[j]:
                return 1 + dfs(i - 1, j - 1)
            # 如果两个字符串的最后一个字符不同，那么最长公共子序列的长度就是两个字符串中去掉最后一个字符之
            # 后的最长公共子序列的长度的较大值
            return max(dfs(i - 1, j), dfs(i, j - 1))

        return dfs(m - 1, n - 1)
