# 3196. Maximize Total Cost of Alternating Subarrays
# https://leetcode.com/problems/maximize-total-cost-of-alternating-subarrays/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def maximumTotalCostDP(self, nums: list[int]) -> int:
        # 空间优化: 滚动 2 个变量代替 dp 数组
        # s1 = dp[i-1], s2 = dp[i]
        n, s1, s2 = len(nums), 0, nums[0]
        for i in range(1, n):
            s = max(s2 + nums[i], s1 + nums[i - 1] - nums[i])
            s1, s2 = s2, s
        return s2

    # time O(n), space O(n)
    def maximumTotalCostDPWithArray(self, nums: list[int]) -> int:
        # 交替子数组的代价: 第一个元素 +, 第二个 -, 第三个 +, ...
        # 可以在任意位置重新开始子数组(重置符号为 +)
        # dp[i+1]: nums[0..i] 的最大总代价
        # 两种选择:
        #   1) nums[i] 符号为 +, 即开始新子数组或延续奇数位: dp[i] + nums[i]
        #   2) nums[i] 符号为 -, 与前一个元素配对: dp[i-1] + nums[i-1] - nums[i]
        n = len(nums)
        dp = [0] * (n + 1)
        dp[1] = nums[0]
        for i in range(1, n):
            dp[i + 1] = max(dp[i] + nums[i], dp[i - 1] + nums[i - 1] - nums[i])
        return dp[n]

    # time O(n), space O(n)
    def maximumTotalCostDFSWithMemorization(self, nums: list[int]) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): nums[0..i] 的最大总代价
        n = len(nums)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            if i == 0:
                return nums[0]
            # 选择 1: nums[i] 取 +    选择 2: nums[i] 取 -, 与 i-1 配对
            return max(dfs(i - 1) + nums[i], dfs(i - 2) + nums[i - 1] - nums[i])

        return dfs(n - 1)
