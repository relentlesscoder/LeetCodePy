# 1458. Max Dot Product of Two Subsequences
# https://leetcode.com/problems/max-dot-product-of-two-subsequences/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(m * n), space O(n)
    def maxDotProduct(self, nums1: list[int], nums2: list[int]) -> int:
        # 继续优化成一个数组
        m = len(nums1)
        n = len(nums2)
        dp = [-inf] * (n + 1)
        for i in range(m):
            pre = dp[0]
            for j in range(n):
                x = dp[j + 1]
                dp[j + 1] = max(max(0, pre) + nums1[i] * nums2[j], dp[j + 1], dp[j])
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def maxDotProductDPWithGrid(self, nums1: list[int], nums2: list[int]) -> int:
        m = len(nums1)
        n = len(nums2)
        dp = [[-inf] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                dp[i + 1][j + 1] = max(
                    max(0, dp[i][j]) + nums1[i] * nums2[j], dp[i][j + 1], dp[i + 1][j]
                )
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def maxDotProductDFSWithMemorization(self, nums1: list[int], nums2: list[int]) -> int:
        m = len(nums1)
        n = len(nums2)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1 or j == -1:  # 其中一个数组空了无法得到点积
                return -inf
            # 选择连接 nums1[i] 和 nums2[j]，得到的点积为 nums1[i] * nums2[j] 加上连接前面元素的最大点积
            # 注意 max(0, dfs(i - 1, j - 1)) 的作用，如果连接前面元素的最大点积为负数，则不连接前面元素
            # 也可以保证只要选了至少一对元素则不会用到 Integer.MIN_VALUE 的值 - 从而满足子序列不为空的要求
            res = max(0, dfs(i - 1, j - 1)) + nums1[i] * nums2[j]
            # 1. 选择不连接 nums1[i]，看看连接 nums1[i - 1] 和 nums2[j] 能得到更大的点积
            # 2. 选择不连接 nums2[j]，看看连接 nums1[i] 和 nums2[j - 1] 能得到更大的点积
            return max(res, dfs(i - 1, j), dfs(i, j - 1))

        return dfs(m - 1, n - 1)
