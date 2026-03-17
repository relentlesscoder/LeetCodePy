# 1639. Number of Ways to Form a Target String Given a Dictionary
# https://leetcode.com/problems/number-of-ways-to-form-a-target-string-given-a-dictionary/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(m * n + k * L), space O(m + n)
    def numWays(self, words: list[str], target: str) -> int:
        # 继续优化成一个数组
        mod = 10**9 + 7
        k = len(words)
        m = 0
        n = len(target)
        for i in range(k):
            m = max(m, len(words[i]))
        # cmap[i][j] = words 数组中第 i 列字符的 frequency 表
        cmap = [[0] * 26 for _ in range(m)]
        for i in range(k):
            for j in range(len(words[i])):
                cmap[j][ord(words[i][j]) - ord("a")] += 1
        dp = [1] + [0] * n
        for i in range(m):
            pre = dp[0]
            dp[0] = 1
            for j in range(n):
                x = dp[j + 1]
                if cmap[i][ord(target[j]) - ord("a")] > 0:
                    dp[j + 1] = (dp[j + 1] + cmap[i][ord(target[j]) - ord("a")] * pre % mod) % mod
                pre = x
        return dp[n]

    # time O(m * n + k * L), space O(m * n)
    def numWaysDPWithGrid(self, words: list[str], target: str) -> int:
        # 把记忆化搜索翻译成 DP
        mod = 10**9 + 7
        k = len(words)
        m = 0
        n = len(target)
        for i in range(k):
            m = max(m, len(words[i]))
        # cmap[i][j] = words 数组中第 i 列字符的 frequency 表
        cmap = [[0] * 26 for _ in range(m)]
        for i in range(k):
            for j in range(len(words[i])):
                cmap[j][ord(words[i][j]) - ord("a")] += 1
        dp = [[1] + [0] * n for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                dp[i + 1][j + 1] = dp[i][j + 1]
                if cmap[i][ord(target[j]) - ord("a")] > 0:
                    dp[i + 1][j + 1] = (
                        dp[i + 1][j + 1] + cmap[i][ord(target[j]) - ord("a")] * dp[i][j] % mod
                    ) % mod
        return dp[m][n]

    # time O(m * n + k * L), space O(m * n)
    def numWaysDFSWithMemorization(self, words: list[str], target: str) -> int:
        # 记忆化搜索
        mod = 10**9 + 7
        k = len(words)
        m = 0
        n = len(target)
        for i in range(k):
            m = max(m, len(words[i]))
        # cmap[i][j] = words 数组中第 i 列字符的 frequency 表
        cmap = [[0] * 26 for _ in range(m)]
        for i in range(k):
            for j in range(len(words[i])):
                cmap[j][ord(words[i][j]) - ord("a")] += 1

        @cache
        def dfs(i: int, j: int) -> int:
            # target 数组先空了说明 words 数组的子序列成功匹配了 target
            if j == -1:
                return 1
            # words 数组先空了说明 words 数组的子序列无法匹配 target
            if i == -1:
                return 0
            # 总是可以选择不用 i 列的字符匹配 target[j]
            res = dfs(i - 1, j)
            # 如果 i 列的字符在 words 数组中存在且等于 target[j]，还可以选择用 i 列的字符匹配 target[j]
            # 注意这里要乘以 cmap[i][ord(target[j]) - ord("a")] 因为 i 列的字符在 words 数组中可能出
            # 现多次
            if cmap[i][ord(target[j]) - ord("a")] > 0:
                res = (res + cmap[i][ord(target[j]) - ord("a")] * dfs(i - 1, j - 1) % mod) % mod
            return res

        return dfs(m - 1, n - 1)
