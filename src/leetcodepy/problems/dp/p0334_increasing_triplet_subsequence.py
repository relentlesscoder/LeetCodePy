# 334. Increasing Triplet Subsequence
# https://leetcode.com/problems/increasing-triplet-subsequence/description/
# Difficulty: Medium


from bisect import bisect_left
from math import inf


class Solution:
    # time O(n), space O(1)
    def increasingTriplet(self, nums: list[int]) -> bool:
        # 贪心法:维护两个变量 m1 和 m2,分别表示当前遍历过的最小值和次小值
        # m1:递增三元组中第一个元素的最小候选值
        # m2:递增三元组中第二个元素的最小候选值(保证 m2 前面一定存在一个比它小的元素)
        # 遍历数组,对每个元素分三种情况讨论:
        #   1. nums[i] <= m1:更新最小值 m1(贪心地让第一个元素尽可能小)
        #   2. m1 < nums[i] < m2:更新次小值 m2(贪心地让第二个元素尽可能小)
        #   3. nums[i] > m2:说明找到了 m1 < m2 < nums[i],递增三元组存在,返回 True
        # 注意:即使 m1 在某次迭代中被更新到 m2 之后的位置,m2 仍然有效,
        # 因为 m2 被赋值时,它前面一定存在一个比它小的旧 m1 值。
        n = len(nums)
        m1 = inf  # 当前最小值
        m2 = inf  # 当前次小值(且保证其前方存在一个更小的元素)
        for i in range(n):
            if nums[i] < m1:
                m1 = nums[i]  # 更新最小值
            elif nums[i] > m1 and nums[i] < m2:
                m2 = nums[i]  # 更新次小值
            elif nums[i] > m2:
                return True  # 找到递增三元组
        return False

    # time O(n * log(n)), space O(n)
    def increasingTripletGreedy(self, nums: list[int]) -> bool:
        # 贪心 + 二分: 同 p0300
        n = len(nums)
        arr = []
        for i in range(n):
            j = bisect_left(arr, nums[i])
            if j == 2:  # 本题只要求三个元素, 可扩展为 k
                return True
            if j == len(arr):
                arr.append(nums[i])
            else:
                arr[j] = nums[i]
        return False
