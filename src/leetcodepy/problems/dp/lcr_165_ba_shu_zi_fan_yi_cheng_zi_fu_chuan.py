# LCR 165. 把数字翻译成字符串
# https://leetcode.cn/problems/ba-shu-zi-fan-yi-cheng-zi-fu-chuan-lcof/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def crackNumberDP(self, ciphertext: int) -> int:
        # 空间优化: 滚动 2 个变量, p0 = dp[i-1], p1 = dp[i]
        s, p0, p1 = str(ciphertext), 0, 1
        n = len(s)
        for i in range(n):
            # 选择 1: 取 1 位, 0-9 对应 a-j, 每位都能单独翻译
            p = p1
            # 选择 2: 取 2 位, 10-25 对应 k-z
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "5")):
                p += p0
            p0, p1 = p1, p
        return p1

    # time O(n), space O(n)
    def crackNumberDPWithArray(self, ciphertext: int) -> int:
        # 类似 p0091, 但更简单: 0-9 都能单独翻译(无 '0' 不可解码的问题)
        # dp[i+1]: s[0..i] 的翻译方案数
        # 取 1 位一定合法; 取 2 位需要在 10-25 范围内
        s = str(ciphertext)
        n = len(s)
        dp = [1] + [0] * n
        for i in range(n):
            dp[i + 1] = dp[i]  # 取 1 位
            # 取 2 位: s[i-1..i] 在 10-25 范围内
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "5")):
                dp[i + 1] += dp[i - 1]
        return dp[n]

    # time O(n), space O(n)
    def crackNumberDFSWithMemorization(self, ciphertext: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的翻译方案数
        s = str(ciphertext)
        n = len(s)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 1
            res = dfs(i - 1)  # 取 1 位
            # 取 2 位
            if i > 0 and (s[i - 1] == "1" or (s[i - 1] == "2" and s[i] <= "5")):
                res += dfs(i - 2)
            return res

        return dfs(n - 1)
