# 494. Target Sum
# https://leetcode.com/problems/target-sum/
# Difficulty: Medium

from functools import cache

class Solution:

    # time O(n * t), space O(t)
    def findTargetSumWaysDP(self, nums: list[int], target: int) -> int:
        # 空间优化版 DP
        n = len(nums)
        t = sum(nums) + target
        if t < 0 or t % 2:
            return 0
        
        m = t // 2
        dp = [1] + [0] * (m)

        for i, x in enumerate(nums):
            for c in range(m, x - 1, -1):
                dp[c] += dp[c - x]
    
        return dp[m]

    # time O(n * t), space O(n * t)
    def findTargetSumWaysDPWithGrid(self, nums: list[int], target: int) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(nums)
        t = sum(nums) + target
        if t < 0 or t % 2:
            return 0
        
        m = t // 2
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        dp[0][0] = 1

        for i, x in enumerate(nums):
            # 从右向左计算使得 dp[c - x] 不会在计算 dp[c] 之前被覆盖
            for c in range(m, -1, -1):
                if c < x:
                    dp[i + 1][c] = dp[i][c]
                else:
                    dp[i + 1][c] = dp[i][c - x] + dp[i][c]
    
        return dp[n][m]

    # time O(n * t), space O(n * t)
    def findTargetSumWaysDFSWithMemorization(self, nums: list[int], target: int) -> int:
        # 记忆化搜索
        t = sum(nums) + target
        if t < 0 or t % 2:
            return 0
        
        @cache
        def dfs(i: int, t: int) -> int:
            if i == -1:
                return 1 if t == 0 else 0
            # 只能不选
            if t < nums[i]:
                return dfs(i - 1, t)
            # 选和不选的总和
            return dfs(i - 1, t - nums[i]) + dfs(i - 1, t)
    
        return dfs(len(nums) - 1, t // 2)
