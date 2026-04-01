# 1438. Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit
# https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/
# Difficulty: Medium


from collections import deque


class Solution:
    # time O(n), space O(n)
    def longestSubarray(self, nums: list[int], limit: int) -> int:
        # 双指针 + 单调队列: 找最长子数组使得 max - min <= limit
        # max - min 就是子数组中最大绝对差
        res, n = 0, len(nums)
        max_queue: deque[int] = deque()  # 单调递减, 队头 = 窗口最大值
        min_queue: deque[int] = deque()  # 单调递增, 队头 = 窗口最小值
        left = 0
        for i in range(n):
            # 维护单调递减队列: 弹出尾部 <= 当前值的元素
            while max_queue and nums[max_queue[-1]] <= nums[i]:
                max_queue.pop()
            max_queue.append(i)
            # 维护单调递增队列: 弹出尾部 >= 当前值的元素
            while min_queue and nums[min_queue[-1]] >= nums[i]:
                min_queue.pop()
            min_queue.append(i)
            # 收缩左边界直到 max - min <= limit
            while nums[max_queue[0]] - nums[min_queue[0]] > limit:
                if max_queue[0] == left:
                    max_queue.popleft()
                if min_queue[0] == left:
                    min_queue.popleft()
                left += 1
            res = max(res, i - left + 1)
        return res
