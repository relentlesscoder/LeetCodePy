# 44. Wildcard Matching
# https://leetcode.com/problems/wildcard-matching/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def isMatch(self, s: str, p: str) -> bool:
        # 继续优化成一个数组
        m = len(s)
        n = len(p)
        dp = [False] * (n + 1)
        dp[0] = True
        for j in range(n):
            dp[j + 1] = dp[j] if p[j] == "*" else False
        for i in range(m):
            pre = dp[0]
            dp[0] = False
            for j in range(n):
                x = dp[j + 1]
                if p[j] == "?" or p[j] == s[i]:
                    dp[j + 1] = pre
                elif p[j] == "*":
                    dp[j + 1] = dp[j] or pre or dp[j + 1]
                else:
                    dp[j + 1] = False
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def isMatchDPWithGrid(self, s: str, p: str) -> bool:
        # 把记忆化搜索翻译成 DP
        m = len(s)
        n = len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for j in range(n):
            dp[0][j + 1] = dp[0][j] if p[j] == "*" else False
        for i in range(m):
            dp[i + 1][0] = False
            for j in range(n):
                if p[j] == "?" or p[j] == s[i]:
                    dp[i + 1][j + 1] = dp[i][j]
                elif p[j] == "*":
                    dp[i + 1][j + 1] = dp[i + 1][j] or dp[i][j] or dp[i][j + 1]
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def isMatchDFSWithMemorization(self, s: str, p: str) -> bool:
        # 记忆化搜索
        m = len(s)
        n = len(p)

        @cache
        def dfs(i: int, j: int) -> int:
            # s 和 p 的最后一个字符都空了说明 s 和 p 成功匹配了
            if i == -1 and j == -1:
                return True
            # p 的最后一个字符空了说明 s 无法匹配 p
            if j == -1:
                return False
            # s 的最后一个字符空了后面只能由 '*' 来匹配空字符否则无法匹配
            if i == -1:
                return dfs(i, j - 1) if p[j] == "*" else False
            # s 的最后一个字符相同或者 p 的最后一个字符是 '?' 则必须匹配
            if p[j] == "?" or p[j] == s[i]:
                return dfs(i - 1, j - 1)
            elif p[j] == "*":
                # 三种情况:
                #   1. '*' 匹配 s 的最后一个字符但保留 '*' 继续往前匹配 - dfs(i - 1, j)
                #   2. '*' 匹配 s 的最后一个字符 - dfs(i - 1, j - 1)
                #   3. '*' 匹配空字符 - dfs(i, j - 1)
                return dfs(i, j - 1) or dfs(i - 1, j - 1) or dfs(i - 1, j)
            return False

        return dfs(m - 1, n - 1)
