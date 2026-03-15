# 72. Edit Distance
# https://leetcode.com/problems/edit-distance/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def minDistance(self, word1: str, word2: str) -> int:
        # 继续优化成一个数组
        m = len(word1)
        n = len(word2)
        dp = list(range(n + 1))
        for i in range(m):
            pre = dp[0]
            dp[0] = i + 1
            for j in range(n):
                x = dp[j + 1]
                if word1[i] == word2[j]:
                    dp[j + 1] = pre
                else:
                    dp[j + 1] = 1 + min(pre, dp[j], dp[j + 1])
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def minDistanceDPWithGrid(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)
        dp = [list(range(n + 1))] + [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            dp[i + 1][0] = i + 1
            for j in range(n):
                if word1[i] == word2[j]:
                    dp[i + 1][j + 1] = dp[i][j]
                else:
                    dp[i + 1][j + 1] = 1 + min(dp[i][j], dp[i + 1][j], dp[i][j + 1])
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def minDistanceDFSWithMemorization(self, word1: str, word2: str) -> int:
        # 记忆化搜索
        m = len(word1)
        n = len(word2)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1 and j == -1:  # 都空了不需要操作
                return 0
            if i == -1 or j == -1:  # 其中一个空了而另一个不空，删除另一个的所有字符
                return i + 1 if j == -1 else j + 1
            if word1[i] == word2[j]:  # 两个字符串的最后一个字符相同，不需要操作
                return dfs(i - 1, j - 1)
            else:
                # 两个字符串的最后一个字符不同，三种情况:
                #   1. 删除 word1 的最后一个字符 - dfs(i - 1, j)
                #   2. 添加一个与 word2 的最后一个字符相同字符到 word1 后面 - dfs(i, j - 1)
                #   3. 替换 word1 的最后一个字符为 word2 的最后一个字符 - dfs(i - 1, j - 1)
                return 1 + min(dfs(i - 1, j - 1), dfs(i, j - 1), dfs(i - 1, j))

        return dfs(m - 1, n - 1)
