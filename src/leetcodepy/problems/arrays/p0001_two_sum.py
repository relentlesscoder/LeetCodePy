# 1. Two Sum
# https://leetcode.com/problems/two-sum/
# Difficulty: Easy
#
# Given an array of integers `nums` and an integer `target`, return indices of
# the two numbers such that they add up to `target`.


class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        seen: dict[int, int] = {}
        for i, n in enumerate(nums):
            complement = target - n
            if complement in seen:
                return [seen[complement], i]
            seen[n] = i
        return []
