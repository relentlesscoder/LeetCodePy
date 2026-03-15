# 3183. The Number of Ways to Make the Sum
# https://leetcode.cn/problems/the-number-of-ways-to-make-the-sum/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(3 * s), space O(s)
    def numberOfWaysSingleDP(self, n: int) -> int:
        # 继续优化:
        #   计算用 6, 2, 1 三种硬币凑成 n 的方案数，也就是不用 4 的方案数，记为 A；
        #   计算用 6, 2, 1 三种硬币凑成 n - 4 的方案数，也就是先用一张面值为 4 的硬币，然后再用 6, 2, 1 三种硬币凑成 n - 4 的方案数，记为 B；
        #   计算用 6, 2, 1 三种硬币凑成 n - 8 的方案数，也就是先用两张面值为 4 的硬币，然后再用 6, 2, 1 三种硬币凑成 n - 8 的方案数，记为 C；
        # 那么答案就是 A + B + C。
        mod = 10**9 + 7
        nums = [6, 2, 1]

        dp = [1] + [0] * n
        for i in range(3):
            for s in range(1, n + 1):
                if nums[i] > s:
                    dp[s] = dp[s]
                else:
                    dp[s] = (dp[s] + dp[s - nums[i]]) % mod
        res = dp[n]
        if n >= 4:
            res = (res + dp[n - 4]) % mod
        if n >= 8:
            res = (res + dp[n - 8]) % mod
        return res

    # time O(9 * s), space O(s)
    def numberOfWaysDPWithArray(self, n: int) -> int:
        # 空间优化版 DP
        mod = 10**9 + 7
        nums = [6, 2, 1]

        res = 0
        for i in range(3):
            if n < 4 * i:
                continue
            dp = [1] + [0] * n
            target = n - 4 * i
            for i in range(3):
                for s in range(1, target + 1):
                    if nums[i] > s:
                        dp[s] = dp[s]
                    else:
                        dp[s] = (dp[s] + dp[s - nums[i]]) % mod
            res = (res + dp[target]) % mod
        return res

    # time O(9 * s), space O(4 * s)
    def numberOfWaysDPWithGrid(self, n: int) -> int:
        # 将记忆化搜索翻译成 DP
        mod = 10**9 + 7
        nums = [6, 2, 1]

        res = 0
        for i in range(3):
            if n < 4 * i:
                continue
            dp = [[1] + [0] * n for _ in range(4)]
            target = n - 4 * i
            for i in range(3):
                for s in range(1, target + 1):
                    if nums[i] > s:
                        dp[i + 1][s] = dp[i][s]
                    else:
                        dp[i + 1][s] = (dp[i][s] + dp[i + 1][s - nums[i]]) % mod
            res = (res + dp[3][target]) % mod
        return res

    # time O(9 * s), space O(3 * s)
    def numberOfWays(self, n: int) -> int:
        # 记忆化搜索
        mod = 10**9 + 7
        nums = [6, 2, 1]  # 无限个硬币的面值 6, 2, 1

        @cache
        def dfs(i: int, s: int) -> int:
            if s == 0:  # 目标金额已经凑成了, 这是一种合法的方案
                return 1
            if (
                i == -1 or nums[i] > s
            ):  # 没有硬币了, 或者当前硬币的面额超过了剩余金额, 这两种情况都不是合法的方案
                return 0
            # 否则可以选择不选这个硬币, 或者选这个硬币
            return (dfs(i - 1, s) + dfs(i, s - nums[i])) % mod

        res = dfs(2, n)  # 先统计用 6, 2, 1 三种硬币凑成 n 的方案数
        if (
            n >= 4
        ):  # 如果 n >= 4, 那么还可以先用一张面值为 4 的硬币, 然后再用 6, 2, 1 三种硬币凑成 n - 4 的方案数
            res = (res + dfs(2, n - 4)) % mod
        if (
            n >= 8
        ):  # 如果 n >= 8, 那么还可以先用两张面值为 4 的硬币, 然后再用 6, 2, 1 三种硬币凑成 n - 8 的方案数
            res = (res + dfs(2, n - 8)) % mod
        return res
