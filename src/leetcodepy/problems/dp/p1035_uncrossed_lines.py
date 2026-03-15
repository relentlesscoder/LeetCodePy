# 1035. Uncrossed Lines
# https://leetcode.com/problems/uncrossed-lines/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(m * n), space O(n)
    def maxUncrossedLines(self, nums1: list[int], nums2: list[int]) -> int:
        # 继续优化成一个数组
        m = len(nums1)
        n = len(nums2)
        dp = [0] * (n + 1)
        for i in range(m):
            pre = dp[0]
            for j in range(n):
                x = dp[j + 1]
                if nums1[i] == nums2[j]:
                    dp[j + 1] = 1 + pre
                else:
                    dp[j + 1] = max(dp[j + 1], dp[j])
                pre = x
        return dp[n]

    # time O(m * n), space O(m * n)
    def maxUncrossedLinesDPWithGrid(self, nums1: list[int], nums2: list[int]) -> int:
        # 把记忆化搜索翻译成 DP
        m = len(nums1)
        n = len(nums2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                if nums1[i] == nums2[j]:
                    dp[i + 1][j + 1] = 1 + dp[i][j]
                else:
                    dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
        return dp[m][n]

    # time O(m * n), space O(m * n)
    def maxUncrossedLinesDFSWithMemorization(self, nums1: list[int], nums2: list[int]) -> int:
        m = len(nums1)
        n = len(nums2)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1 or j == -1:  # 其中一个数组空了无法连线
                return 0
            if nums1[i] == nums2[j]:  # 两个数组的最后一个字符相同可以连线
                return 1 + dfs(i - 1, j - 1)
            else:  # 两个数组的最后一个字符不同则只能舍弃其中一个数组的最后一个元素
                return max(dfs(i - 1, j), dfs(i, j - 1))

        return dfs(m - 1, n - 1)
