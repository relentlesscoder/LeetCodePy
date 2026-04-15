# 2786. Visit Array Positions to Maximize Score
# https://leetcode.com/problems/visit-array-positions-to-maximize-score/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n), space O(1)
    def maxScoreDP(self, nums: list[int], x: int) -> int:
        # 滚动变量 DP. pre[j] = 到目前为止, 最后访问的奇偶性为 j 的最大得分.
        # 初始: 必须访问 nums[0], 只有 nums[0]%2 那一侧合法.
        n = len(nums)
        pre = [-inf, -inf]
        pre[nums[0] % 2] = nums[0]  # 必须访问 nums[0]
        for i in range(1, n, 1):
            dp = [-inf, -inf]
            for j in range(2):
                if j == nums[i] % 2:
                    # 奇偶性匹配, 可以访问 i 或跳过
                    # 访问: nums[i] + max(同奇偶无惩罚, 异奇偶扣 x)
                    visit = max(pre[j], pre[1 ^ j] - x) + nums[i]
                    dp[j] = max(pre[j], visit)  # 跳过 vs 访问
                else:
                    # 奇偶性不匹配, 跳过
                    dp[j] = pre[j]
            pre = dp
        return max(pre[0], pre[1])

    # time O(n), space O(n)
    def maxScoreDPWithGrid(self, nums: list[int], x: int) -> int:
        # 数组 DP, 显式保存每步状态, 便于理解.
        # dp[i][j]: 从 nums[0..i] 中选子序列, 最后访问的奇偶性为 j 的最大得分.
        n = len(nums)
        dp = [[-inf, -inf] for _ in range(n)]
        dp[0][nums[0] % 2] = nums[0]  # 必须访问 nums[0]
        for i in range(1, n, 1):
            for j in range(2):
                if j == nums[i] % 2:
                    # 奇偶性匹配, 可以访问 i 或跳过
                    visit = max(dp[i - 1][j], dp[i - 1][1 ^ j] - x) + nums[i]
                    dp[i][j] = max(dp[i - 1][j], visit)
                else:
                    # 奇偶性不匹配, 跳过
                    dp[i][j] = dp[i - 1][j]
        return max(dp[n - 1][0], dp[n - 1][1])

    # time O(n), space O(n)
    def maxScoreDFSWithMemorization(self, nums: list[int], x: int) -> int:
        # 子序列选取 DP (非状态机). 必须访问 nums[0], 按顺序选子序列,
        # 相邻访问的元素奇偶性不同时扣 x 分, 求最大得分.
        # dfs(i, j): 从 nums[0..i] 中选子序列, 最后访问的奇偶性为 j 的最大得分.
        # 每个位置的决策: 访问或跳过.
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == 0:
                # 必须访问 nums[0], 奇偶性匹配才合法
                return nums[0] if j == nums[0] % 2 else -inf
            if j == nums[i] % 2:
                # 奇偶性匹配, 可以访问 i 或跳过
                # 访问: nums[i] + max(前一个同奇偶, 前一个异奇偶扣 x)
                visit = max(dfs(i - 1, j), dfs(i - 1, 1 ^ j) - x) + nums[i]
                skip = dfs(i - 1, j)  # 跳过 i, 最后访问的奇偶性不变
                return max(visit, skip)
            # 奇偶性不匹配, i 不可能是最后访问的 (否则 j 应为 nums[i]%2), 跳过
            return dfs(i - 1, j)

        # 最后访问的元素可能是偶数或奇数, 两种情况取最大
        return max(dfs(n - 1, 0), dfs(n - 1, 1))
