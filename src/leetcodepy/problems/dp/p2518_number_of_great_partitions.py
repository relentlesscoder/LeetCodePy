# 2518. Number of Great Partitions
# https://leetcode.com/problems/number-of-great-partitions/
# Difficulty: Hard

from functools import cache


class Solution:
    # time O(n * k), space O(k)
    def countPartitions(self, nums: list[int], k: int) -> int:
        # 空间优化版 DP
        mod = 10**9 + 7
        n = len(nums)
        s = sum(nums)
        if s < 2 * k:
            return 0

        # dp[0] = 0 (v=0 说明和已 >= k 不是坏子集), dp[1..k] = 1
        dp = [0] + [1] * k
        for i in range(n):
            for c in range(k, -1, -1):
                dp[c] = (dp[c] + (dp[c - nums[i]] if c > nums[i] else 0)) % mod

        return (pow(2, n, mod) - 2 * dp[k]) % mod

    # time O(n * k), space O(n * k)
    def countPartitionsDPWithGrid(self, nums: list[int], k: int) -> int:
        # 将记忆化搜索翻译成 DP
        mod = 10**9 + 7
        n = len(nums)
        s = sum(nums)
        if s < 2 * k:
            return 0

        # dp[0][0] = 0 (v=0 说明和已 >= k 不是坏子集), dp[0][1..k] = 1
        dp = [[0] + [1] * k] + [[0] * (k + 1) for _ in range(n)]
        for i in range(n):
            for c in range(k, -1, -1):
                dp[i + 1][c] = (dp[i][c] + (dp[i][c - nums[i]] if c > nums[i] else 0)) % mod

        return (pow(2, n, mod) - 2 * dp[n][k]) % mod

    # time O(n * k), space O(k)
    def countPartitionsDFSWithMemorization(self, nums: list[int], k: int) -> int:
        # 记忆化搜索: 题目要求分成两个子集且每个子集的和都 >= k, 等价于统计有多少子集的和 < k
        # 的方案数, 然后用总方案数减去这个数就是答案了。
        mod = 10**9 + 7
        n = len(nums)
        s = sum(nums)
        if s < 2 * k:
            return 0

        @cache
        def dfs(i: int, v: int) -> int:
            # v <= 0 说明当前子集的和已经 >= k, 后续无论怎么选都不是"坏"子集, 剪枝
            if v <= 0:
                return 0
            if i == -1:
                return 1  # v > 0 说明和 < k, 是"坏"子集
            return (dfs(i - 1, v - nums[i]) + dfs(i - 1, v)) % mod

        return (pow(2, n, mod) - 2 * dfs(n - 1, k)) % mod
