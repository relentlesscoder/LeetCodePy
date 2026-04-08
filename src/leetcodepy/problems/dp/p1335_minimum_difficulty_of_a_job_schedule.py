# 1335. Minimum Difficulty of a Job Schedule
# https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(d * n^2), space O(n)
    def minDifficultyDP(self, jobDifficulty: list[int], d: int) -> int:
        # 1D 滚动数组 DP. 将任务分成恰好 d 天, 最小化每天最大难度之和.
        # dp[j+1] 表示将 jobs[0..j] 分成若干天时, 总难度的最小值.
        # 每轮 i 对应"再增加一天", 枚举当天起点 x, 状态转移为:
        #   dp[j+1] = min(max(jobs[x..j]) + dp[x])  for x in [i, j]
        # 注意: 这是 min-sum 问题, 不能用二分答案, 只能 DP.
        n = len(jobDifficulty)
        if n < d:
            return -1  # 任务数 < 天数, 每天至少一个任务, 无解
        dp = [0] + [inf] * n
        for i in range(d):
            for j in range(n - 1, i - 1, -1):  # 从右向左保证本轮只用上一轮的值
                res, diff = inf, 0
                for x in range(j, i - 1, -1):  # 枚举当天起点, 同时维护区间最大值
                    diff = max(diff, jobDifficulty[x])
                    # 当天难度 max(jobs[x..j]) + 前面天的最优值
                    res = min(res, diff + dp[x])
                dp[j + 1] = res
        return dp[n]

    # time O(d * n^2), space O(d * n)
    def minDifficultyDPWithGrid(self, jobDifficulty: list[int], d: int) -> int:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示将 jobs[0..j] 分成恰好 i+1 天时, 总难度的最小值.
        n = len(jobDifficulty)
        if n < d:
            return -1
        dp = [[0] + [inf] * n] + [[inf] * (n + 1) for _ in range(d)]
        for i in range(d):
            for j in range(n - 1, i - 1, -1):
                res, diff = inf, 0
                for x in range(j, i - 1, -1):
                    diff = max(diff, jobDifficulty[x])
                    # 引用上一轮 dp[i][x], 即前 x 个任务分成 i 天的最优值
                    res = min(res, diff + dp[i][x])
                dp[i + 1][j + 1] = res
        return dp[d][n]

    # time O(d * n^2), space O(d * n)
    def minDifficultyDFSWithMemorization(self, jobDifficulty: list[int], d: int) -> int:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j) 表示将 jobs[0..j] 分成恰好 i+1 天时, 总难度的最小值.
        n = len(jobDifficulty)
        if n < d:
            return -1

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == -1 else inf  # 天数用完: 任务也恰好分完则合法
            if j == -1:
                return inf  # 任务已空但还需分天, 不合法
            res, diff = inf, 0
            for x in range(j, i - 1, -1):  # 枚举当天起点 x
                diff = max(diff, jobDifficulty[x])
                # 当天难度 max(jobs[x..j]) + 前面天的最优值
                res = min(res, diff + dfs(i - 1, x - 1))
            return res

        return dfs(d - 1, n - 1)
