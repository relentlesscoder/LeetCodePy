# 712. Minimum ASCII Delete Sum for Two Strings
# https://leetcode.com/problems/minimum-ascii-delete-sum-for-two-strings/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def minimumDeleteSumDPWithSingleArray(self, s1: str, s2: str) -> int:
        # 继续优化成一个数组
        m = len(s1)
        n = len(s2)
        dp = [0] * (n + 1)
        # 预处理 s2 前缀和，计算 s1 为空时 s2 剩下的字符的 ASCII 码之和
        for i in range(n):
            dp[i + 1] = dp[i] + ord(s2[i])
        for i in range(m):
            pre = dp[0]  # dp[i - 1][j - 1]
            dp[0] += ord(s1[i])  # dp[i][0] 实时更新 s1 前缀 ASCII 码之和
            for j in range(n):
                x = dp[j + 1]  # 在被覆盖之前先保存 dp[i - 1][j] 的值
                if s1[i] == s2[j]:  # 两个字符串的最后一个字符相同，不需要删除继续比较前面的字符
                    dp[j + 1] = pre
                else:  # 两个字符串的最后一个字符不同，需要删除其中一个字符串的最后一个字符继续比较
                    dp[j + 1] = min(ord(s1[i]) + dp[j + 1], ord(s2[j]) + dp[j])
                pre = x  # 更新 pre 的值为计算下一个格子需要的 dp[i - 1][j - 1] 的值
        return dp[n]

    # time O(m * n), space O(n)
    def minimumDeleteSumDPWithRollingArray(self, s1: str, s2: str) -> int:
        # 空间优化版 DP
        m = len(s1)
        n = len(s2)
        dp = [0] * (n + 1)
        for i in range(n):
            dp[i + 1] = dp[i] + ord(s2[i])
        for i in range(m):
            next = [dp[0] + ord(s1[i])] + [0] * (n)
            for j in range(n):
                if s1[i] == s2[j]:
                    next[j + 1] = dp[j]
                else:
                    next[j + 1] = min(ord(s1[i]) + dp[j + 1], ord(s2[j]) + next[j])
            dp = next
        return dp[n]

    # time O(m * n), space O(m * n)
    def minimumDeleteSumDPWithGrid(self, s1: str, s2: str) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(s1)
        n = len(s2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(n):
            dp[0][i + 1] = dp[0][i] + ord(s2[i])
        for i in range(m):
            dp[i + 1][0] = dp[i][0] + ord(s1[i])
            for j in range(n):
                if s1[i] == s2[j]:
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = min(ord(s1[i]) + dp[i][j + 1], ord(s2[j]) + dp[i + 1][j])
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def minimumDeleteSumDFSWithMemorization(self, s1: str, s2: str) -> int:
        # 记忆化搜索
        m = len(s1)
        n = len(s2)
        pre1 = [0] * (m + 1)
        pre2 = [0] * (n + 1)
        # 预处理前缀和，方便计算删除一个字符串剩下的字符的 ASCII 码之和
        for i, c in enumerate(s1):
            pre1[i + 1] = pre1[i] + ord(c)
        for i, c in enumerate(s2):
            pre2[i + 1] = pre2[i] + ord(c)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1 and j == -1:  # 都空了，不需要删除任何字符
                return 0
            if i == -1:  # s1 空了 s2 不空，需要删除 s2 的所有字符
                return pre2[j + 1]
            if j == -1:  # s2 空了 s1 不空，需要删除 s1 的所有字符
                return pre1[i + 1]
            if s1[i] == s2[j]:  # 两个字符串的最后一个字符相同，不需要删除
                return dfs(i - 1, j - 1)
            else:  # 两个字符串的最后一个字符不同，需要删除其中一个字符串的最后一个字符并继续比较
                return min(ord(s1[i]) + dfs(i - 1, j), ord(s2[j]) + dfs(i, j - 1))

        return dfs(m - 1, n - 1)
