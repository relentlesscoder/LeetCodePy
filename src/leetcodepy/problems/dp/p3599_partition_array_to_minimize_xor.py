# 3599. Partition Array to Minimize XOR
# https://leetcode.com/problems/partition-array-to-minimize-xor/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    def minXorDP(self, nums: list[int], k: int) -> int:
        n = len(nums)
        dp = [0] + [inf] * n
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res, xor = inf, 0
                for x in range(j, i - 1, -1):
                    xor ^= nums[x]
                    if xor >= res:
                        continue
                    res = min(res, max(xor, dp[x]))
                dp[j + 1] = res
        return dp[n]

    def minXorDPWithGrid(self, nums: list[int], k: int) -> int:
        n = len(nums)
        dp = [[0] + [inf] * n] + [[0] * (n + 1) for _ in range(k)]
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res, xor = inf, 0
                for x in range(j, i - 1, -1):
                    xor ^= nums[x]
                    if xor >= res:
                        continue
                    res = min(res, max(xor, dp[i][x]))
                dp[i + 1][j + 1] = res
        return dp[k][n]

    def minXorDFSWithMemorization(self, nums: list[int], k: int) -> int:
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == -1 else inf
            if j == -1:
                return inf
            res, xor = inf, 0
            for x in range(j, -1, -1):
                xor ^= nums[x]
                if xor >= res:
                    continue
                res = min(res, max(xor, dfs(i - 1, x - 1)))
            return res

        return dfs(k - 1, n - 1)
