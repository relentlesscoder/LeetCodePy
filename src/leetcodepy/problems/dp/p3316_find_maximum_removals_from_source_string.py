# 3316. Find Maximum Removals From Source String
# https://leetcode.com/problems/find-maximum-removals-from-source-string/
# Difficulty: Medium


from bisect import bisect_right
from functools import cache
from math import inf


class Solution:
    # time O(m * n), space O(n)
    def maxRemovals(self, source: str, pattern: str, targetIndices: list[int]) -> int:
        # 继续优化成一个数组
        m = len(source)
        n = len(pattern)
        idx = set(targetIndices)
        dp = [0] + [-inf] * n
        for i in range(m):
            x = 1 if i in idx else 0
            pre = dp[0]
            dp[0] += x
            for j in range(n):
                c = dp[j + 1]
                dp[j + 1] += x
                if source[i] == pattern[j]:
                    dp[j + 1] = max(dp[j + 1], pre)
                pre = c
        return dp[n]

    # time O(m * n), space O(m * n)
    def maxRemovalsDPWithGrid(self, source: str, pattern: str, targetIndices: list[int]) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(source)
        n = len(pattern)
        idx = set(targetIndices)
        dp = [[0] + [-inf] * n] + [[0] * (n + 1) for _ in range(m)]
        for i in range(m):
            x = 1 if i in idx else 0
            dp[i + 1][0] = dp[i][0] + x
            for j in range(n):
                dp[i + 1][j + 1] = dp[i][j + 1] + x
                if source[i] == pattern[j]:
                    dp[i + 1][j + 1] = max(dp[i + 1][j + 1], dp[i][j])
        return dp[m][n]

    # time O(m * n * log(t)), space O(m * n)
    def maxRemovalsDFSWithMemorization(
        self, source: str, pattern: str, targetIndices: list[int]
    ) -> int:
        # 记忆化搜索
        m = len(source)
        n = len(pattern)
        idx = set(targetIndices)

        @cache
        def dfs(i: int, j: int) -> int:
            # pattern 数组先空了说明 source 数组的子序列成功匹配了 pattern,
            # targetIndices 中剩余的元素都可以被删除
            if j == -1:
                return bisect_right(targetIndices, i)
            # source 数组先空了说明 source 数组的子序列无法匹配 pattern
            if i == -1:
                return -inf
            # 选择不匹配 source[i]，如果 source[i] 在 targetIndices 中则
            # 删除 source[i]
            res = dfs(i - 1, j) + (1 if i in idx else 0)
            # 选择匹配 source[i] 和 pattern[j]
            if source[i] == pattern[j]:
                res = max(res, dfs(i - 1, j - 1))
            return res

        return dfs(m - 1, n - 1)
