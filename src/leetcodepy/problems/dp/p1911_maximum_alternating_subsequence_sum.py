# 1911. Maximum Alternating Subsequence Sum
# https://leetcode.com/problems/maximum-alternating-subsequence-sum/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxAlternatingSumDP(self, nums: list[int]) -> int:
        # 子序列选取 DP, 滚动变量. 选子序列使交替和最大.
        # 交替和 = a[0] - a[1] + a[2] - ... (奇数位加, 偶数位减).
        # 等价于股票买卖: +nums[i] = 买入获利, -nums[i] = 卖出付出.
        # d0: 以偶数位结尾的最大交替和
        # d1: 以奇数位结尾 (或空序列) 的最大交替和
        # 初始: d0 = -inf (还没选过, 不合法), d1 = 0 (空序列合法).
        n, d0, d1 = len(nums), -inf, 0
        for i in range(n):
            c0 = max(d0, d1 + nums[i])  # 跳过 or 从 d1 选为偶数位 (+nums[i])
            c1 = max(d1, d0 - nums[i])  # 跳过 or 从 d0 选为奇数位 (-nums[i])
            d0 = c0
            d1 = c1
        return max(d0, d1)

    # time O(n), space O(n)
    def maxAlternatingSumDPWithGrid(self, nums: list[int]) -> int:
        # 数组 DP, 显式保存每步状态, 便于理解.
        # dp[i+1][0]: 从 nums[0..i] 选子序列, 以偶数位结尾的最大交替和
        # dp[i+1][1]: 从 nums[0..i] 选子序列, 以奇数位结尾或空的最大交替和
        n = len(nums)
        dp = [[-inf, 0]] + [[-inf, -inf] for _ in range(n)]
        for i in range(n):
            dp[i + 1][0] = max(dp[i][0], dp[i][1] + nums[i])  # 跳过 or 从状态1选为偶数位 (+)
            dp[i + 1][1] = max(dp[i][1], dp[i][0] - nums[i])  # 跳过 or 从状态0选为奇数位 (-)
        return max(dp[n][0], dp[n][1])

    # time O(n), space O(n)
    def maxAlternatingSumDFSWithMemorization(self, nums: list[int]) -> int:
        # 记忆化搜索 (自顶向下), 与数组 DP 等价.
        # dfs(i, j): 从 nums[0..i] 选子序列, 当前状态为 j 的最大交替和.
        #   j=0: 以偶数位结尾.
        #   j=1: 以奇数位结尾或空.
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == 1 else -inf  # j=1 (空序列) 合法, j=0 还没选过不合法
            if j == 0:
                # 以偶数位结尾: 跳过 or 从状态1选为偶数位 (+nums[i])
                return max(dfs(i - 1, 0), dfs(i - 1, 1) + nums[i])
            # 以奇数位结尾或空: 跳过 or 从状态0选为奇数位 (-nums[i])
            return max(dfs(i - 1, 1), dfs(i - 1, 0) - nums[i])

        # 最后一个选的可能是奇数位或偶数位
        return max(dfs(n - 1, 0), dfs(n - 1, 1))
