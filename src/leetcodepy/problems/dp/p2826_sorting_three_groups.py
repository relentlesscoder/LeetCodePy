# 2826. Sorting Three Groups
# https://leetcode.com/problems/sorting-three-groups/
# Difficulty: Medium


from bisect import bisect_right
from functools import cache


class Solution:
    # time O(n * log(n)), space O(n)
    def minimumOperationsGreedy(self, nums: list[int]) -> int:
        # 贪心 + 二分: 同 p0300, 但这里是非递减子序列, 所以 bisect_right
        n = len(nums)
        arr = []
        for i in range(n):
            idx = bisect_right(arr, nums[i])
            if idx == len(arr):
                arr.append(nums[i])
            else:
                arr[idx] = nums[i]
        return n - len(arr)

    # time O(n^2), space O(n)
    def minimumOperationsDP(self, nums: list[int]) -> int:
        # 把记忆化搜索改成 DP
        n = len(nums)
        dp = [0] * n
        for i in range(n):
            mx = 0
            for j in range(i):
                if nums[i] >= nums[j]:
                    mx = max(mx, dp[j])
            dp[i] = mx + 1
        return n - max(dp[i] for i in range(n))

    # time O(n^2), space O(n)
    def minimumOperationsDFSWithMemorization(self, nums: list[int]) -> int:
        # 转化为最长非递减子序列(LIS 变体)问题:
        # nums 中值只有 1, 2, 3, 要让数组变为非递减,
        # 最少操作次数 = n - 最长非递减子序列长度
        # dfs(i): 以 nums[i] 结尾的最长非递减子序列长度
        # 转移: 在 j < i 中找 nums[j] <= nums[i] 的最大 dfs(j), 加 1
        n = len(nums)

        @cache
        def dfs(i: int) -> int:
            res = 0
            for j in range(i):
                if nums[i] >= nums[j]:
                    res = max(res, dfs(j))
            return res + 1

        return n - max(dfs(i) for i in range(n))
