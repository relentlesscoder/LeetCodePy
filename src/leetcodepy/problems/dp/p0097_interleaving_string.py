# 97. Interleaving String
# https://leetcode.com/problems/interleaving-string/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        # 继续优化成一个数组
        m = len(s1)
        n = len(s2)
        k = len(s3)
        if m + n != k:
            return False
        dp = [False] * (n + 1)
        dp[0] = True
        for j in range(0, n):
            dp[j + 1] = s2[j] == s3[j] and dp[j]
        for i in range(m):
            dp[0] = s1[i] == s3[i] and dp[0]
            for j in range(n):
                dp[j + 1] = (s1[i] == s3[i + j + 1] and dp[j + 1]) or (
                    s2[j] == s3[i + j + 1] and dp[j]
                )
        return dp[n]

    # time O(m * n), space O(m * n)
    def isInterleaveDPWithGrid(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        k = len(s3)
        if m + n != k:
            return False
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for j in range(0, n):
            dp[0][j + 1] = s2[j] == s3[j] and dp[0][j]
        for i in range(m):
            dp[i + 1][0] = s1[i] == s3[i] and dp[i][0]
            for j in range(n):
                dp[i + 1][j + 1] = (s1[i] == s3[i + j + 1] and dp[i][j + 1]) or (
                    s2[j] == s3[i + j + 1] and dp[i + 1][j]
                )
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def isInterleaveDFSWithMemorization(self, s1: str, s2: str, s3: str) -> bool:
        m = len(s1)
        n = len(s2)
        k = len(s3)
        # s1 和 s2 的长度之和必须等于 s3 的长度才能交错组成 s3
        if m + n != k:
            return False

        @cache
        def dfs(i: int, j: int) -> int:
            # s1 和 s2 的最后一个字符都空了说明 s1 和 s2 的子序列成功匹配了 s3
            if i == -1 and j == -1:
                return True
            # s2 的最后一个字符空了后面只能由 s1 的子序列来匹配 s3
            if j == -1:
                return s1[i] == s3[i + j + 1] and dfs(i - 1, j)
            # s1 的最后一个字符空了后面只能由 s2 的子序列来匹配 s3
            if i == -1:
                return s2[j] == s3[i + j + 1] and dfs(i, j - 1)
            # s1 和 s2 的最后一个字符都不空了可以选择用 s1 的最后一个字符匹配 s3
            # 的最后一个字符或者用 s2 的最后一个字符匹配 s3 的最后一个字符, 注意
            # 匹配的前提是必须与 s3 的最后一个字符相同
            b1 = s1[i] == s3[i + j + 1] and dfs(i - 1, j)
            b2 = s2[j] == s3[i + j + 1] and dfs(i, j - 1)
            return b1 or b2

        return dfs(m - 1, n - 1)
