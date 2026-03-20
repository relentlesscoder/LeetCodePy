# 3825. Longest Strictly Increasing Subsequence With Non-Zero Bitwise AND
# https://leetcode.com/problems/longest-strictly-increasing-subsequence-with-non-zero-bitwise-and/
# Difficulty: Hard


from bisect import bisect_left


class Solution:
    # time O(m * n * log(n)), space O(n)
    def longestSubsequence(self, nums: list[int]) -> int:
        # 要求子序列的 AND 非零, 即至少存在某一位 i 所有元素的第 i 位都为 1
        # 枚举每一位 i, 只保留第 i 位为 1 的元素, 求最长严格递增子序列(LIS)
        # 所有位的 LIS 取最大值即为答案
        res = 0
        n = len(nums)
        mx = 0
        for i in range(n):
            mx = max(mx, nums[i])
        m = mx.bit_length()  # 最大值的二进制位数
        for i in range(m):
            # 对第 i 位为 1 的元素求 LIS (贪心 + 二分)
            arr = []  # 贪心维护的严格递增数组
            for j in range(n):
                if (1 << i) & nums[j] != 0:
                    # bisect_left: 严格递增, 找第一个 >= nums[j] 的位置
                    idx = bisect_left(arr, nums[j])
                    if idx == len(arr):
                        arr.append(nums[j])
                    else:
                        arr[idx] = nums[j]
            res = max(res, len(arr))
        return res
