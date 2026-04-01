# 813. Largest Sum of Averages
# https://leetcode.com/problems/largest-sum-of-averages/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(k * n^2), space O(n)
    def largestSumOfAveragesDP(self, nums: list[int], k: int) -> float:
        # 1D 滚动数组 DP. 将数组分成恰好 k 段, 求各段平均值之和的最大值.
        # dp[j+1] 表示将 nums[0..j] 分成若干段时, 平均值之和的最大值.
        # 每轮 i 对应"再增加一段"的决策, 枚举最后一段的起点 x, 状态转移为:
        #   dp[j+1] = max(avg(nums[x..j]) + dp[x])  for x in [0, j]
        # 初始 dp[0]=0 (空前缀合法), dp[1..n]=-inf (尚未被任何段覆盖).
        n = len(nums)
        dp = [0] + [-inf] * n
        for i in range(k):
            for j in range(n - 1, i - 1, -1):  # 从右向左保证本轮只用上一轮的值
                res, total, cnt = 0, 0, 0
                for x in range(j, -1, -1):  # 枚举最后一段的起点, 同时累积区间和
                    total += nums[x]
                    cnt += 1
                    # avg(nums[x..j]) + 前 x 个元素已分好的最优值
                    res = max(res, total / cnt + dp[x])
                dp[j + 1] = res
        return dp[n]

    # time O(k * n^2), space O(k * n)
    def largestSumOfAveragesDPWithGrid(self, nums: list[int], k: int) -> float:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示将 nums[0..j] 分成恰好 i+1 段时的最大平均值之和.
        # dp[0] 初始化: dp[0][0]=0, dp[0][1..n]=-inf, 表示"0 段划分"只对空前缀合法.
        n = len(nums)
        dp = [[0] + [-inf] * n] + [[0] * (n + 1) for _ in range(k)]
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res, total, cnt = 0, 0, 0
                for x in range(j, -1, -1):
                    total += nums[x]
                    cnt += 1
                    # 引用上一轮 dp[i][x], 即前 x 个元素分成 i 段的最优值
                    res = max(res, total / cnt + dp[i][x])
                dp[i + 1][j + 1] = res
        return dp[k][n]

    # time O(k * n^2), space O(k * n)
    def largestSumOfAveragesDFSWithMemorization(self, nums: list[int], k: int) -> float:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j) 表示将 nums[0..j] 分成恰好 i+1 段时的最大平均值之和.
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> float:
            if j == -1:
                return 0  # 空前缀, 无论几段都为 0 (段数也应为 0)
            if i == -1:
                return -inf  # 还需继续分段但前缀已耗尽, 不合法
            res, total, cnt = 0, 0, 0
            for x in range(j, -1, -1):  # 枚举最后一段起点 x
                total += nums[x]
                cnt += 1
                # 最后一段 avg(nums[x..j]) + 前 x 个元素分成 i 段的最优值
                res = max(res, total / cnt + dfs(i - 1, x - 1))
            return res

        return dfs(k - 1, n - 1)
