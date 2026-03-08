# 643. Maximum Average Subarray I
# https://leetcode.com/problems/maximum-average-subarray-i/
# Difficulty: Easy

from math import inf


class Solution:
    
    # time O(n), space O(1)
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        res = -inf
        sum = 0
        for i, c in enumerate(nums):
            sum += c

            left = i - k + 1
            if left < 0:
                continue
            
            res = max(res, sum)
            sum -= nums[left]
    
        return res / k
