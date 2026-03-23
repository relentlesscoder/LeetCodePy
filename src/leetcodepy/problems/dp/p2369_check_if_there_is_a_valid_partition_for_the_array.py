# 2369. Check if There is a Valid Partition For The Array
# https://leetcode.com/problems/check-if-there-is-a-valid-partition-for-the-array/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def validPartitionDP(self, nums: list[int]) -> bool:
        # 空间优化: 滚动 3 个变量代替 dp 数组
        # b0 = dp[i-2], b1 = dp[i-1], b2 = dp[i]
        n = len(nums)
        b0 = False  # dp[-1] 无意义
        b1 = True  # dp[0] = True (空数组)
        b2 = False  # dp[1] = False (单个元素无法划分)
        for i in range(1, n):
            c = False
            # 取 2 个: dp[i+1] |= dp[i-1]
            if nums[i - 1] == nums[i]:
                c = b1
            # 取 3 个: dp[i+1] |= dp[i-2]
            if i >= 2 and (
                (nums[i - 1] == nums[i] and nums[i - 2] == nums[i - 1])
                or (nums[i - 1] + 1 == nums[i] and nums[i - 2] + 1 == nums[i - 1])
            ):
                c = c or b0
            b0, b1, b2 = b1, b2, c
        return b2

    # time O(n), space O(n)
    def validPartitionDPWithArray(self, nums: list[int]) -> bool:
        # 将记忆化搜索翻译为自底向上 DP
        # dp[i+1]: nums[0..i] 能否被合法划分 (偏移 1 方便处理边界)
        # dp[0] = True (空数组), dp[1] = False (单个元素)
        n = len(nums)
        dp = [True] + [False] * (n)
        for i in range(1, n):
            # 取末尾 2 个 [a,a]: dp[i+1] |= dp[i-1]
            if nums[i - 1] == nums[i]:
                dp[i + 1] = dp[i - 1]
            # 取末尾 3 个 [a,a,a] 或 [a,a+1,a+2]: dp[i+1] |= dp[i-2]
            if i >= 2 and (
                (nums[i - 1] == nums[i] and nums[i - 2] == nums[i - 1])
                or (nums[i - 1] + 1 == nums[i] and nums[i - 2] + 1 == nums[i - 1])
            ):
                dp[i + 1] = dp[i + 1] or dp[i - 2]
        return dp[n]

    # time O(n), space O(n)
    def validPartitionDFSWithMemorization(self, nums: list[int]) -> bool:
        # 三种合法子数组: [a,a], [a,a,a], [a,a+1,a+2]
        # dfs(i): nums[0..i] 能否被合法划分
        # 从末尾尝试取 2 个或 3 个元素, 检查是否合法, 递归剩余部分
        n = len(nums)

        @cache
        def dfs(i: int) -> bool:
            if i == -1:
                return True  # 空数组, 合法
            if i == 0:
                return False  # 只剩一个元素, 无法构成任何合法子数组
            res = False
            # 取末尾 2 个: [a, a]
            if i >= 1 and nums[i - 1] == nums[i]:
                res = res or dfs(i - 2)
            # 取末尾 3 个: [a, a, a] 或 [a, a+1, a+2]
            if i >= 2 and (
                (nums[i - 1] == nums[i] and nums[i - 2] == nums[i - 1])
                or (nums[i - 1] + 1 == nums[i] and nums[i - 2] + 1 == nums[i - 1])
            ):
                res = res or dfs(i - 3)
            return res

        return dfs(n - 1)
