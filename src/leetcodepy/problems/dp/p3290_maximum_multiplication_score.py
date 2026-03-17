# 3290. Maximum Multiplication Score
# https://leetcode.com/problems/maximum-multiplication-score/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(m * n), space O(n)
    def maxScore(self, a: list[int], b: list[int]) -> int:
        # 继续优化成一个数组
        m = len(a)
        n = len(b)
        dp = [0] * (n + 1)
        for i in range(m):
            pre = dp[0]
            dp[0] = -inf
            for j in range(n):
                x = dp[j + 1]
                dp[j + 1] = max(a[i] * b[j] + pre, dp[j])
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def maxScoreDPWithGrid(self, a: list[int], b: list[int]) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(a)
        n = len(b)
        dp = [[0] * (n + 1)] + [[-inf] * (n + 1) for _ in range(m)]
        for i in range(m):
            for j in range(n):
                dp[i + 1][j + 1] = max(a[i] * b[j] + dp[i][j], dp[i + 1][j])
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def maxScoreDFSWithMemorization(self, a: list[int], b: list[int]) -> int:
        # 记忆化搜索
        m = len(a)
        n = len(b)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:  # a 数组先空了返回当前点积
                return 0
            if j == -1:  # b 数组先空了则无法得到点积
                return -inf  # 返回负无穷保证不选任何元素的点积不会被选中从而满足子序列不为空的要求
            # 选择 a[i] * b[j] 加上连接前面元素的最大点积
            return max(a[i] * b[j] + dfs(i - 1, j - 1), dfs(i, j - 1))

        return dfs(m - 1, n - 1)
