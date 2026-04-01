# 3144. Minimum Substring Partition of Equal Character Frequency
# https://leetcode.com/problems/minimum-substring-partition-of-equal-character-frequency/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n^2), space O(n)
    def minimumSubstringsInPartitionDP(self, s: str) -> int:
        # 将字符串分成最少的子串, 使每个子串中所有出现的字符频率相同
        # dp[i+1]: s[0..i] 的最少划分段数
        # 从 i 往前枚举子串 s[j..i], 维护字符频率判断是否合法
        n = len(s)
        dp = [0] * (n + 1)
        for i in range(n):
            res, mx, k = inf, 0, 0
            freq = [0] * 26  # 字符频率
            for j in range(i, -1, -1):
                idx = ord(s[j]) - ord("a")
                if freq[idx] == 0:
                    k += 1  # k: 不同字符个数
                freq[idx] += 1
                mx = max(mx, freq[idx])  # mx: 最大频率
                # 合法条件: 最大频率 * 字符种数 == 子串长度
                # 即所有出现的字符频率都等于 mx
                if mx * k == i - j + 1:
                    res = min(res, 1 + dp[j])
            dp[i + 1] = res
        return dp[n]

    # time O(n^2), space O(n)
    def minimumSubstringsInPartitionDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的最少划分段数
        n = len(s)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            res, mx, k = inf, 0, 0
            freq = [0] * 26
            for j in range(i, -1, -1):
                idx = ord(s[j]) - ord("a")
                if freq[idx] == 0:
                    k += 1
                freq[idx] += 1
                mx = max(mx, freq[idx])
                if mx * k == i - j + 1:
                    res = min(res, 1 + dfs(j - 1))
            return res

        return dfs(n - 1)
