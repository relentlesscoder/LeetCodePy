# 1278. Palindrome Partitioning III
# https://leetcode.com/problems/palindrome-partitioning-iii/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(n^2 + k * n^2) = O(k * n^2), space O(n^2)
    def palindromePartitionDP(self, s: str, k: int) -> int:
        # 1D 滚动数组 DP. 将字符串分成恰好 k 段, 最小化将每段变回文的总替换次数.
        # 预处理 cost[i][j]: 把 s[i..j] 变成回文的最小替换次数
        # dp[j+1] 表示将 s[0..j] 分成若干段时, 总替换次数的最小值.
        # 每轮 i 对应"再增加一段", 枚举最后一段起点 x, 状态转移为:
        #   dp[j+1] = min(cost[x][j] + dp[x])  for x in [i, j]
        n = len(s)
        cost = [[0] * n for _ in range(n)]
        for length in range(2, n + 1):  # 按区间长度从小到大预处理
            for i in range(n - length + 1):
                j = i + length - 1
                cost[i][j] = cost[i + 1][j - 1] + (s[i] != s[j])
        dp = [0] + [inf] * n
        for i in range(k):
            for j in range(n - 1, i - 1, -1):  # 从右向左保证本轮只用上一轮的值
                res = inf
                for x in range(j, i - 1, -1):  # 枚举最后一段起点
                    # 最后一段 s[x..j] 的回文代价 + 前面段的最优值
                    res = min(res, cost[x][j] + dp[x])
                dp[j + 1] = res
        return dp[n]

    # time O(k * n^2), space O(n^2 + k * n)
    def palindromePartition(self, s: str, k: int) -> int:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示将 s[0..j] 分成恰好 i+1 段时, 总替换次数的最小值.
        n = len(s)
        cost = [[0] * n for _ in range(n)]
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                cost[i][j] = cost[i + 1][j - 1] + (s[i] != s[j])
        dp = [[0] + [inf] * n] + [[inf] * (n + 1) for _ in range(k)]
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res = inf
                for x in range(j, i - 1, -1):
                    # 引用上一轮 dp[i][x], 即前 x 个字符分成 i 段的最优值
                    res = min(res, cost[x][j] + dp[i][x])
                dp[i + 1][j + 1] = res
        return dp[k][n]

    # time O(k * n^2), space O(n^2 + k * n)
    def palindromePartitionDFSWithMemorization(self, s: str, k: int) -> int:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j) 表示将 s[0..j] 分成恰好 i+1 段时, 总替换次数的最小值.
        n = len(s)
        cost = [[0] * n for _ in range(n)]
        for l in range(2, n + 1):
            for i in range(n - l + 1):
                j = i + l - 1
                cost[i][j] = cost[i + 1][j - 1] + (s[i] != s[j])

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == -1 else inf  # 段数用完: 前缀也恰好为空则合法
            if j == -1:
                return inf  # 前缀已空但还需分段, 不合法
            res = inf
            for x in range(j, -1, -1):  # 枚举最后一段起点 x
                # 最后一段 s[x..j] 的回文代价 + 前面段的最优值
                res = min(res, cost[x][j] + dfs(i - 1, x - 1))
            return res

        return dfs(k - 1, n - 1)
