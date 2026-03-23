# 354. Russian Doll Envelopes
# https://leetcode.com/problems/russian-doll-envelopes/
# Difficulty: Hard


from bisect import bisect_left


class Solution:
    # time O(n * log(n)), space O(n)
    def maxEnvelopes(self, envelopes: list[list[int]]) -> int:
        # 转化为一维 LIS 问题:
        # 按宽度升序排序, 宽度相同时按高度降序排序
        # 这样宽度相同的信封最多只能选一个(因为高度是降序的, LIS 不会同时选中)
        # 排序后只需对高度求严格递增子序列(LIS)
        n = len(envelopes)
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        # 贪心 + 二分求 LIS
        nums = []
        for i in range(n):
            idx = bisect_left(nums, envelopes[i][1])
            if idx == len(nums):
                nums.append(envelopes[i][1])
            else:
                nums[idx] = envelopes[i][1]
        return len(nums)
