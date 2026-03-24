# 91. Decode Ways
# https://leetcode.com/problems/decode-ways/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def numDecodingsDP(self, s: str) -> int:
        # 空间优化: 滚动 2 个变量, s1 = dp[i-1], s2 = dp[i]
        n, s1, s2 = len(s), 0, 1
        for i in range(n):
            res = 0
            # 选择 1: s[i] 单独解码 (1-9), '0' 不能单独解码
            if s[i] != "0":
                res += s2
            # 选择 2: s[i-1..i] 两位解码 (10-26)
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "6")):
                res += s1
            s1, s2 = s2, res
        return s2

    # time O(n), space O(n)
    def numDecodingsDPWithArray(self, s: str) -> int:
        # A-Z 对应 1-26, 每个位置可以取 1 位或 2 位数字解码
        # dp[i+1]: s[0..i] 的解码方案数
        # dp[0] = 1 (空串, 一种方案)
        n = len(s)
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(n):
            res = 0
            # 取 1 位: s[i] 对应 1-9
            if s[i] != "0":
                res += dp[i]
            # 取 2 位: s[i-1..i] 对应 10-26
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "6")):
                res += dp[i - 1]
            dp[i + 1] = res
        return dp[n]

    # time O(n), space O(n)
    def numDecodingsDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的解码方案数
        n = len(s)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 1  # 空串, 一种方案
            res = 0
            # 取 1 位
            if s[i] != "0":
                res += dfs(i - 1)
            # 取 2 位
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "6")):
                res += dfs(i - 2)
            return res

        return dfs(n - 1)
