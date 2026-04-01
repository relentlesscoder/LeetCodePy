# 1043. Partition Array for Maximum Sum
# https://leetcode.com/problems/partition-array-for-maximum-sum/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n * k), space O(n)
    def maxSumAfterPartitioningDPWithArray(self, arr: list[int], k: int) -> int:
        # 将数组分成若干子数组, 每个子数组长度 <= k
        # 每个子数组的值全部替换为该子数组的最大值, 求替换后总和最大值
        # dp[i+1]: arr[0..i] 的最大总和
        # 枚举最后一个子数组 arr[j..i], 长度 1 到 k
        # 该子数组贡献 = max(arr[j..i]) * (i - j + 1)
        n = len(arr)
        dp = [0] * (n + 1)
        for i in range(n):
            res, mx = 0, 0
            for j in range(i, max(i - k, -1), -1):
                mx = max(mx, arr[j])  # 从 i 往前扩展, 维护区间最大值
                res = max(res, mx * (i - j + 1) + dp[j])
            dp[i + 1] = res
        return dp[n]

    # time O(n * k), space O(n)
    def maxSumAfterPartitioningDFSWithMemorization(self, arr: list[int], k: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): arr[0..i] 的最大总和
        n = len(arr)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            res, mx = 0, 0
            # 枚举最后一个子数组长度 1 到 k
            for j in range(i, max(i - k, -1), -1):
                mx = max(mx, arr[j])
                res = max(res, mx * (i - j + 1) + dfs(j - 1))
            return res

        return dfs(n - 1)
