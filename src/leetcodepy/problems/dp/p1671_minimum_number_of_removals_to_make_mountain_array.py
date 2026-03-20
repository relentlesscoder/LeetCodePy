# 1671. Minimum Number of Removals to Make Mountain Array
# https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/
# Difficulty: Hard


from bisect import bisect_left


class Solution:
    # time O(n * log(n)), space O(n)
    def minimumMountainRemovals(self, nums: list[int]) -> int:
        # 山形数组: 先严格递增再严格递减, 峰顶左右至少各有一个元素
        # 思路: 对每个位置 i, 求以 i 结尾的 LIS 长度(left) 和以 i 开头的 LDS 长度(right)
        # 以 i 为峰顶的最长山形长度 = left[i] + right[i] - 1 (峰顶计算了两次)
        # 最少删除数 = n - 最长山形长度
        max_mountain = 0
        n = len(nums)
        # left[i]: 从左到右, 以 nums[i] 结尾的 LIS 长度
        left = self.lisAtEachPosition(nums)
        # 反转后求 LIS = 原数组从右到左的 LDS
        nums.reverse()
        # 继续优化还可以节省一个数组，不想写了
        right = self.lisAtEachPosition(nums)
        for i in range(n):
            # 峰顶左右必须各有至少一个元素, 即 left/right 都 > 1
            if left[i] <= 1 or right[n - 1 - i] <= 1:
                continue
            max_mountain = max(max_mountain, left[i] + right[n - 1 - i] - 1)
        return n - max_mountain

    def lisAtEachPosition(self, nums: list[int]) -> list[int]:
        # 贪心 + 二分: 同 p0300, 但这里是严格递增子序列, 所以 bisect_left
        n = len(nums)
        res = [0] * (n)
        arr = []
        for i in range(n):
            idx = bisect_left(arr, nums[i])
            res[i] = idx + 1
            if idx == len(arr):
                arr.append(nums[i])
            else:
                arr[idx] = nums[i]
        return res
