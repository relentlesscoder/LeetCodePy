# 1049. Last Stone Weight II
# https://leetcode.com/problems/last-stone-weight-ii/
# Difficulty: Medium

from functools import cache


class Solution:
    # time O(n * t), space O(t)
    def lastStoneWeightIIDP(self, stones: list[int]) -> int:
        # 空间优化版 DP
        n = len(stones)
        s = sum(stones)
        t = s // 2

        dp = list(range(t + 1))

        for i, x in enumerate(stones):
            # 从右向左计算使得 dp[c - x] 不会在计算 dp[c] 之前被覆盖
            for c in range(t, -1, -1):
                dp[c] = min(dp[c - x] if c >= x else 10000, dp[c])

        return s - 2 * (t - dp[t])

    # time O(n * t), space O(n * t)
    def lastStoneWeightIIDPWithGrid(self, stones: list[int]) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(stones)
        s = sum(stones)
        t = s // 2

        dp = [[0] * (t + 1) for _ in range(n + 1)]
        dp[0] = list(range(t + 1))

        for i, x in enumerate(stones):
            for c in range(t, -1, -1):
                dp[i + 1][c] = min(dp[i][c - x] if c >= x else 10000, dp[i][c])

        return s - 2 * (t - dp[n][t])

    # time O(n * t), space O(n * t)
    def lastStoneWeightIIDFSWithMemorization(self, stones: list[int]) -> int:
        # 记忆化搜索 - 可以转化为将石头分成两堆，假设小的那一堆的和为 x 则最后剩下的
        # 重量为 (sum - x) - x = sum - 2 * x 。转化为求 x 在不大于 sum / 2
        # 条件下的最大值 - 这是 0/1 背包问题。
        n = len(stones)
        s = sum(stones)
        t = s // 2

        @cache
        def dfs(i: int, target: int) -> int:
            if target < 0:
                return 10000
            if i == -1:
                return target
            return min(dfs(i - 1, target - stones[i]), dfs(i - 1, target))

        return s - 2 * (t - dfs(n - 1, t))
