# 1416. Restore The Array
# https://leetcode.com/problems/restore-the-array/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(n * log10(k)), space O(n)
    def numberOfArraysDP(self, s: str, k: int) -> int:
        # 将数字字符串分成若干部分, 每部分表示 [1, k] 范围内的数(无前导零)
        # dp[i+1]: s[0..i] 的合法分割方案数
        # 从 i 往前枚举最后一段 s[j..i], 逐位构建数字判断是否 <= k
        n, mod, m = len(s), 10**9 + 7, len(str(k))
        dp = [1] + [0] * n
        for i in range(n):
            res, num, x = 0, 0, 1  # num: 当前构建的数字, x: 位权(1, 10, 100, ...)
            # 内层最多走 m 步(k 的位数), 超过位数一定 > k
            for j in range(i, max(i - m, -1), -1):
                if s[j] == "0":
                    x *= 10
                    continue  # 前导零不合法, 跳过但继续往前
                d = ord(s[j]) - ord("0")
                num += d * x  # 从低位到高位构建数字
                if num > k:
                    break
                res = (res + dp[j]) % mod
                x *= 10
            dp[i + 1] = res
        return dp[n]

    # time O(n * log10(k)), space O(n)
    def numberOfArraysDFSWithMemorization(self, s: str, k: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的合法分割方案数
        n, mod, m = len(s), 10**9 + 7, len(str(k))

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 1
            res, num, x = 0, 0, 1
            for j in range(i, max(i - m, -1), -1):
                if s[j] == "0":
                    x *= 10
                    continue
                d = ord(s[j]) - ord("0")
                num += d * x
                if num > k:
                    break
                res = (res + dfs(j - 1)) % mod
                x *= 10
            return res

        return dfs(n - 1)
