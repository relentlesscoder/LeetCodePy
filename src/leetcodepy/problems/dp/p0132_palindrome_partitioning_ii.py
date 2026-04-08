# 132. Palindrome Partitioning II
# https://leetcode.com/problems/palindrome-partitioning-ii/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(n^2), space O(n)
    def minCutDPWithCentralExpansion(self, s: str) -> int:
        # 中心扩展 + DP: 省去 O(n^2) 的回文预处理数组
        # dp[i+1]: s[0..i] 的最少划分段数
        # 从每个中心 m 向两边扩展, 找到回文 s[j..i] 时更新 dp[i+1]
        # 最终答案 = 段数 - 1 = 切割次数
        n = len(s)
        dp = [0] + [inf] * n
        for m in range(n):
            # 奇数长度回文: 以 m 为中心
            j, i = m, m
            while j >= 0 and i < n and s[i] == s[j]:
                dp[i + 1] = min(dp[i + 1], dp[j] + 1)
                i += 1
                j -= 1
            # 偶数长度回文: 以 m, m+1 为中心
            j, i = m, m + 1
            while j >= 0 and i < n and s[i] == s[j]:
                dp[i + 1] = min(dp[i + 1], dp[j] + 1)
                i += 1
                j -= 1
        return dp[n] - 1

    # time O(n^2), space O(n^2)
    def minCutDP(self, s: str) -> int:
        # 两步: 1) 预处理回文表 2) DP 求最少划分段数
        n = len(s)
        # is_palin[i][j]: s[i..j] 是否回文
        # 从后往前填, 保证 is_palin[i+1][j-1] 在使用时已计算
        is_palin = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                is_palin[i][j] = s[i] == s[j] and (j - i <= 2 or is_palin[i + 1][j - 1])
        # dp[i+1]: s[0..i] 的最少划分段数
        dp = [0] * (n + 1)
        for i in range(n):
            res = inf
            for j in range(i + 1):
                if is_palin[j][i]:
                    # s[j..i] 是回文, 前面 s[0..j-1] 需要 dp[j] 段
                    res = min(res, 1 + dp[j])
            dp[i + 1] = res
        return dp[n] - 1

    # time O(n^2), space O(n^2)
    def minCutDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 minCutDP
        # dfs(i): s[0..i] 的最少划分段数
        n = len(s)
        is_palin = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n):
                is_palin[i][j] = s[i] == s[j] and (j - i <= 2 or is_palin[i + 1][j - 1])

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0  # 空串, 0 段
            res = inf
            for j in range(i + 1):
                if is_palin[j][i]:
                    res = min(res, 1 + dfs(j - 1))
            return res

        return dfs(n - 1) - 1
