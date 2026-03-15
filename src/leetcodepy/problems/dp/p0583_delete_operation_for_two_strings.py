# 583. Delete Operation for Two Strings
# https://leetcode.com/problems/delete-operation-for-two-strings/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def minDistanceDPWithSingleArray(self, word1: str, word2: str) -> int:
        # 继续优化成一个数组
        m = len(word1)
        n = len(word2)
        dp = list(range(n + 1))
        for i in range(m):
            pre = dp[0]  # dp[i - 1][j - 1]
            dp[0] = i + 1  # dp[i][0]
            for j in range(n):
                x = dp[j + 1]  # 在被覆盖之前先保存 dp[i - 1][j] 的值
                if (
                    word1[i] == word2[j]
                ):  # 两个字符串的最后一个字符相同，不需要删除继续比较前面的字符
                    dp[j + 1] = pre
                else:  # 两个字符串的最后一个字符不同，需要删除其中一个字符串的最后一个字符继续比较
                    dp[j + 1] = 1 + min(dp[j], dp[j + 1])
                pre = x  # 更新 pre 的值为计算下一个格子需要的 dp[i - 1][j - 1] 的值
        return dp[n]

    # time O(m * n), space O(n)
    def minDistanceDPWithRollingArray(self, word1: str, word2: str) -> int:
        # 空间优化版 DP
        m = len(word1)
        n = len(word2)
        dp = list(range(n + 1))
        for i in range(m):
            next = [i + 1] + [0] * n
            for j in range(n):
                if word1[i] == word2[j]:
                    next[j + 1] = dp[j]
                else:
                    next[j + 1] = 1 + min(next[j], dp[j + 1])
            dp = next
        return dp[n]

    # time O(m * n), space O(m * n)
    def minDistanceDFSWithGrid(self, word1: str, word2: str) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(word1)
        n = len(word2)
        dp = [list(range(n + 1))] + [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            dp[i + 1][0] = i + 1
            for j in range(n):
                if word1[i] == word2[j]:
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = 1 + min(dp[i + 1][j], dp[i][j + 1])
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def minDistanceDFSWithMemorization(self, word1: str, word2: str) -> int:
        # 记忆化搜索
        m = len(word1)
        n = len(word2)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1 and j == -1:  # 都空了，不需要删除任何字符
                return 0
            if i == -1 or j == -1:  # 其中一个空了，另一个不空，需要删除另一个的所有字符
                return i + 1 if j == -1 else j + 1
            if word1[i] == word2[j]:  # 两个字符串的最后一个字符相同，不需要删除，继续比较前面的字符
                return dfs(i - 1, j - 1)
            else:  # 两个字符串的最后一个字符不同，需要删除其中一个字符串的最后一个字符，继续比较
                return 1 + min(dfs(i - 1, j), dfs(i, j - 1))

        return dfs(m - 1, n - 1)
