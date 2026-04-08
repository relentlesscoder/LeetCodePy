# 3599. Partition Array to Minimize XOR
# https://leetcode.com/problems/partition-array-to-minimize-xor/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(k * n^2), space O(n)
    def minXorDP(self, nums: list[int], k: int) -> int:
        # 1D 滚动数组 DP. 将数组分成恰好 k 段, 最小化所有段 XOR 值的最大值.
        # dp[j+1] 表示将 nums[0..j] 分成若干段时, 各段 XOR 最大值的最小值.
        # 每轮 i 对应"再增加一段"的决策, 枚举最后一段起点 x, 状态转移为:
        #   dp[j+1] = min(max(xor(nums[x..j]), dp[x]))  for x in [i, j]
        # 目标是 minimax: 取所有段中 XOR 最大的那个, 让它尽量小.
        n = len(nums)
        dp = [0] + [inf] * n
        for i in range(k):
            for j in range(n - 1, i - 1, -1):  # 从右向左保证本轮只用上一轮的值
                res, xor = inf, 0
                for x in range(j, i - 1, -1):  # 枚举最后一段起点, 同时累积 XOR
                    xor ^= nums[x]
                    if xor >= res:  # 剪枝: 当前段 XOR 已不优于已知最优, 跳过
                        continue
                    # max(当前段 XOR, 前面段的最优 minimax) 取较小者
                    res = min(res, max(xor, dp[x]))
                dp[j + 1] = res
        return dp[n]

    # time O(k * n^2), space O(k * n)
    def minXorDPWithGrid(self, nums: list[int], k: int) -> int:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示将 nums[0..j] 分成恰好 i+1 段时, 各段 XOR 最大值的最小值.
        # dp[0] 初始化: dp[0][0]=0 (空前缀合法), dp[0][1..n]=inf (0 段无法覆盖非空前缀).
        n = len(nums)
        dp = [[0] + [inf] * n] + [[0] * (n + 1) for _ in range(k)]
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res, xor = inf, 0
                for x in range(j, i - 1, -1):
                    xor ^= nums[x]
                    if xor >= res:
                        continue
                    # 引用上一轮 dp[i][x], 即前 x 个元素分成 i 段的最优值
                    res = min(res, max(xor, dp[i][x]))
                dp[i + 1][j + 1] = res
        return dp[k][n]

    # time O(k * n^2), space O(k * n)
    def minXorDFSWithMemorization(self, nums: list[int], k: int) -> int:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j) 表示将 nums[0..j] 分成恰好 i+1 段时, 各段 XOR 最大值的最小值.
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == -1 else inf  # 段数用完: 前缀也恰好为空则合法, 否则不合法
            if j == -1:
                return inf  # 前缀已空但还需分段, 不合法
            res, xor = inf, 0
            for x in range(j, -1, -1):  # 枚举最后一段起点 x
                xor ^= nums[x]
                if xor >= res:  # 剪枝
                    continue
                # max(最后一段 XOR, 前面段的最优 minimax) 取较小者
                res = min(res, max(xor, dfs(i - 1, x - 1)))
            return res

        return dfs(k - 1, n - 1)
