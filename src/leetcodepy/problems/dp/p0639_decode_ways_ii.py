# 639. Decode Ways II
# https://leetcode.com/problems/decode-ways-ii/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(n), space O(1)
    def numDecodingsDP(self, s: str) -> int:
        # 空间优化: 滚动 2 个变量, s1 = dp[i-1], s2 = dp[i]
        n, mod, s1, s2 = len(s), 10**9 + 7, 0, 1
        for i in range(n):
            res = 0
            # --- 取 1 位: s[i] 单独解码 ---
            if s[i] >= "1" and s[i] <= "9":
                res = (res + s2) % mod
            elif s[i] == "*":
                res = (res + 9 * s2) % mod  # * 代表 1-9, 9 种
            # --- 取 2 位: s[i-1..i] 两位解码 ---
            if i > 0:
                if s[i - 1] == "*" and s[i] == "*":
                    res = (res + 15 * s1) % mod  # ** → 11-19(9) + 21-26(6) = 15
                elif s[i - 1] == "1" and s[i] == "*":
                    res = (res + 9 * s1) % mod  # 1* → 11-19 = 9
                elif s[i - 1] == "2" and s[i] == "*":
                    res = (res + 6 * s1) % mod  # 2* → 21-26 = 6
                elif s[i - 1] == "*" and s[i] >= "0" and s[i] <= "6":
                    res = (res + 2 * s1) % mod  # *0-*6 → 1x 或 2x = 2
                elif (
                    (s[i - 1] == "*" and s[i] >= "7" and s[i] <= "9")
                    or (s[i - 1] == "1" and s[i] >= "0" and s[i] <= "9")
                    or (s[i - 1] == "2" and s[i] >= "0" and s[i] <= "6")
                ):
                    res = (res + s1) % mod  # *7-*9 → 只有 1x; 10-19; 20-26 = 1
            s1, s2 = s2, res
        return s2

    # time O(n), space O(n)
    def numDecodingsDPWithArray(self, s: str) -> int:
        # p0091 的扩展: * 代表 1-9, 需要分类讨论
        # dp[i+1]: s[0..i] 的解码方案数
        n, mod = len(s), 10**9 + 7
        dp = [0] * (n + 1)
        dp[0] = 1
        for i in range(n):
            res = 0
            # 取 1 位
            if s[i] >= "1" and s[i] <= "9":
                res = (res + dp[i]) % mod
            elif s[i] == "*":
                res = (res + 9 * dp[i]) % mod
            # 取 2 位
            if i > 0:
                if s[i - 1] == "*" and s[i] == "*":
                    res = (res + 15 * dp[i - 1]) % mod
                elif s[i - 1] == "1" and s[i] == "*":
                    res = (res + 9 * dp[i - 1]) % mod
                elif s[i - 1] == "2" and s[i] == "*":
                    res = (res + 6 * dp[i - 1]) % mod
                elif s[i - 1] == "*" and s[i] >= "0" and s[i] <= "6":
                    res = (res + 2 * dp[i - 1]) % mod
                elif (
                    (s[i - 1] == "*" and s[i] >= "7" and s[i] <= "9")
                    or (s[i - 1] == "1" and s[i] >= "0" and s[i] <= "9")
                    or (s[i - 1] == "2" and s[i] >= "0" and s[i] <= "6")
                ):
                    res = (res + dp[i - 1]) % mod
            dp[i + 1] = res
        return dp[n]

    # time O(n), space O(n)
    def numDecodingsDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的解码方案数
        n, mod = len(s), 10**9 + 7

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 1
            res = 0
            # 取 1 位
            if s[i] >= "1" and s[i] <= "9":
                res = (res + dfs(i - 1)) % mod
            elif s[i] == "*":
                res = (res + 9 * dfs(i - 1)) % mod
            # 取 2 位
            if i > 0:
                if s[i - 1] == "*" and s[i] == "*":
                    res = (res + 15 * dfs(i - 2)) % mod
                elif s[i - 1] == "1" and s[i] == "*":
                    res = (res + 9 * dfs(i - 2)) % mod
                elif s[i - 1] == "2" and s[i] == "*":
                    res = (res + 6 * dfs(i - 2)) % mod
                elif s[i - 1] == "*" and s[i] >= "0" and s[i] <= "6":
                    res = (res + 2 * dfs(i - 2)) % mod
                elif (
                    (s[i - 1] == "*" and s[i] >= "7" and s[i] <= "9")
                    or (s[i - 1] == "1" and s[i] >= "0" and s[i] <= "9")
                    or (s[i - 1] == "2" and s[i] >= "0" and s[i] <= "6")
                ):
                    res = (res + dfs(i - 2)) % mod
            return res

        return dfs(n - 1)
