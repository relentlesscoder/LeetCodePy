# 3647. Maximum Weight in Two Bags
# https://leetcode.com/problems/maximum-weight-in-two-bags/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n * w1 * w2), space O(w1 * w2)
    def maxWeight(self, weights: list[int], w1: int, w2: int) -> int:
        # 空间优化版 DP
        n = len(weights)
        dp = [[0] * (w2 + 1) for _ in range(w1 + 1)]

        for i in range(w1, -1, -1):
            for j in range(w2, -1, -1):
                dp[i][j] = i + j

        for i in range(n):
            for j in range(w1, -1, -1):
                for k in range(w2, -1, -1):
                    if j >= weights[i]:
                        dp[j][k] = min(dp[j][k], dp[j - weights[i]][k])
                    if k >= weights[i]:
                        dp[j][k] = min(dp[j][k], dp[j][k - weights[i]])

        return w1 + w2 - dp[w1][w2]

    # time O(n * w1 * w2), space O(n * w1 * w2)
    def maxWeightDPWithGrid(self, weights: list[int], w1: int, w2: int) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(weights)
        dp = [[[0] * (w2 + 1) for _ in range(w1 + 1)] for _ in range(n + 1)]

        for i in range(w1, -1, -1):
            for j in range(w2, -1, -1):
                dp[0][i][j] = i + j

        for i in range(n):
            for j in range(w1, -1, -1):
                for k in range(w2, -1, -1):
                    dp[i + 1][j][k] = dp[i][j][k]
                    if j >= weights[i]:
                        dp[i + 1][j][k] = min(dp[i + 1][j][k], dp[i][j - weights[i]][k])
                    if k >= weights[i]:
                        dp[i + 1][j][k] = min(dp[i + 1][j][k], dp[i][j][k - weights[i]])

        return w1 + w2 - dp[n][w1][w2]

    # time O(n * w1 * w2), space O(n * w1 * w2)
    def maxWeightDFSWithMemorization(self, weights: list[int], w1: int, w2: int) -> int:
        # 记忆化搜索
        n = len(weights)
        weights.sort(reverse=True)  # 先将物品按重量从大到小排序, 这样在搜索过程中就能尽早剪枝

        @cache
        def dfs(i: int, j: int, k: int) -> int:
            if i == -1 or max(j, k) < weights[i]:
                return j + k
            res = dfs(i - 1, j, k)  # 不选这个物品
            if j >= weights[i]:  # 选这个物品放在第一个背包
                res = min(res, dfs(i - 1, j - weights[i], k))
            if k >= weights[i]:  # 选这个物品放在第二个背包
                res = min(res, dfs(i - 1, j, k - weights[i]))
            return res

        return w1 + w2 - dfs(n - 1, w1, w2)
