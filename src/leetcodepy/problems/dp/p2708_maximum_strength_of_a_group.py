# 2708. Maximum Strength of a Group
# https://leetcode.com/problems/maximum-strength-of-a-group/
# Difficulty: Medium


class Solution:
    # time O(n), space O(1)
    def maxStrength(self, nums: list[int]) -> int:
        # 线性 DP, 滚动变量. 选非空子集使乘积最大.
        # 类似 p0152 (最大子数组乘积), 但这里是子集而非子数组.
        # 同时维护 mx (最大乘积) 和 mn (最小乘积, 可能是负数).
        # 需要 mn 是因为负数 * 负数 = 正数, 可能翻转为最大值.
        # 对每个 nums[i], 四种选择:
        #   1) 不选 i: 保留 mx/mn
        #   2) 只选 i: nums[i] 自身
        #   3) 选 i 并组合: nums[i] * mx 或 nums[i] * mn
        n = len(nums)
        min_prod, max_prod = nums[0], nums[0]
        for i in range(1, n, 1):
            p1, p2 = max_prod * nums[i], min_prod * nums[i]
            min_prod = min(min_prod, nums[i], p1, p2)
            max_prod = max(max_prod, nums[i], p1, p2)
        return max_prod
