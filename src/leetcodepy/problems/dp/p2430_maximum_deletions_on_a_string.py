# 2430. Maximum Deletions on a String
# https://leetcode.com/problems/maximum-deletions-on-a-string/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(n^2), space O(n)
    def deleteStringRollingHash(self, s: str) -> int:
        # Rolling Hash: 用哈希值 O(1) 比较两个子串是否相等
        # 预处理前缀哈希和幂次数组
        # hash(s[i..j]) = hash[j+1] - hash[i] * pow[j-i+1]
        n, mod, base = len(s), 10**9 + 7, 131
        hash = [0] * (n + 1)
        pow = [1] + [0] * n
        for i in range(n):
            hash[i + 1] = (hash[i] * base + ord(s[i])) % mod
            pow[i + 1] = pow[i] * base % mod

        # dp[i]: 从位置 i 开始的最大删除次数
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            res = 0
            # j = 删除的前缀长度, 需要 s[i:i+j] == s[i+j:i+2j]
            for j in range(1, (n - i) // 2 + 1, 1):
                h1 = (hash[i + j] - hash[i] * pow[j] % mod + mod) % mod
                h2 = (hash[i + 2 * j] - hash[i + j] * pow[j] % mod + mod) % mod
                if h1 == h2:
                    res = max(res, dp[i + j])
            dp[i] = res + 1
        return dp[0]

    # time O(n^2), space O(n^2)
    def deleteStringDP(self, s: str) -> int:
        # LCP + DP: 预处理最长公共前缀, O(1) 判断子串是否相等
        # lcp[i][j]: s[i:] 和 s[j:] 的最长公共前缀长度
        # s[i:i+j] == s[i+j:i+2j] 等价于 lcp[i][i+j] >= j
        n = len(s)
        lcp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1
        # dp[i]: 从位置 i 开始的最大删除次数
        # 每次删除长度 j 的前缀, 要求前缀等于删除后的前缀
        dp = [0] * n
        for i in range(n - 1, -1, -1):
            res = 0
            for j in range(1, (n - i) // 2 + 1, 1):
                if lcp[i][i + j] >= j:
                    res = max(res, dp[i + j])
            dp[i] = res + 1  # +1: 最后一次删除整个剩余字符串
        return dp[0]

    # time O(n^2), space O(n^2)
    def deleteStringDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): 从位置 i 开始的最大删除次数
        n = len(s)
        lcp = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            for j in range(n - 1, i, -1):
                if s[i] == s[j]:
                    lcp[i][j] = lcp[i + 1][j + 1] + 1

        @cache
        def dfs(i: int) -> int:
            if i == n:
                return 0
            res = 0
            for j in range(1, (n - i) // 2 + 1, 1):
                if lcp[i][i + j] >= j:
                    res = max(res, dfs(i + j))
            return res + 1

        return dfs(0)
