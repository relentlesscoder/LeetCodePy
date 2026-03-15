# 718. Maximum Length of Repeated Subarray
# https://leetcode.com/problems/maximum-length-of-repeated-subarray/
# Difficulty: Medium


class Solution:
    # time O(m * n), space O(n)
    def findLengthDP(self, nums1: list[int], nums2: list[int]) -> int:
        # 继续优化成一个数组
        m = len(nums1)
        n = len(nums2)
        res = 0
        dp = [0] * (n + 1)
        for i in range(m):
            pre = dp[0]
            for j in range(n):
                x = dp[j + 1]
                if nums1[i] == nums2[j]:
                    dp[j + 1] = 1 + pre
                    res = max(res, dp[j + 1])
                else:
                    dp[j + 1] = 0
                pre = x
        return res

    # time O(m * n), space O(m * n)
    def findLengthDPWithGrid(self, nums1: list[int], nums2: list[int]) -> int:
        m = len(nums1)
        n = len(nums2)
        res = 0
        # dp[i + 1][j + 1] 表示以 nums1[i] 和 nums2[j] 结尾的最长公共子数组的长度
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                # 只有当 nums1[i] 和 nums2[j] 相等时才能延长公共子数组的长度
                if nums1[i] == nums2[j]:
                    dp[i + 1][j + 1] = 1 + dp[i][j]
                    # 更新结果
                    res = max(res, dp[i + 1][j + 1])
        return res
