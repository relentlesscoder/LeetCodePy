# 2209. Minimum White Tiles After Covering With Carpets
# https://leetcode.com/problems/minimum-white-tiles-after-covering-with-carpets/
# Difficulty: Hard


from functools import cache


class Solution:
    # time O(numCarpets * n), space O(n)
    def minimumWhiteTilesDPWithRollingArray(
        self, floor: str, numCarpets: int, carpetLen: int
    ) -> int:
        # 滚动数组 DP. 用 numCarpets 块长度为 carpetLen 的地毯覆盖地板,
        # 最小化剩余白色瓷砖数 (floor[j]=='1' 为白色).
        # pre[j+1] 表示用 i 块地毯覆盖 floor[0..j] 后的最少白色瓷砖数.
        # 初始 pre = 白色瓷砖前缀和 (0 块地毯时直接计数).
        # 每轮 i 增加一块地毯, 对每个位置 j 决策:
        #   1) 不铺地毯: dp[j] + (floor[j]=='1'), 白色瓷砖数累加
        #   2) 铺地毯覆盖 floor[j-carpetLen+1..j]: pre[j-carpetLen+1]
        # 当 j < (i+1)*carpetLen 时, i+1 块地毯足以覆盖所有位置, 结果为 0.
        n = len(floor)
        pre = [0] * (n + 1)
        for i in range(n):
            pre[i + 1] = pre[i] + (1 if floor[i] == "1" else 0)
        for i in range(numCarpets):
            dp = [0] * (n + 1)
            for j in range(n):
                if j < (i + 1) * carpetLen:  # 地毯足够覆盖所有位置
                    continue
                dp[j + 1] = min(
                    pre[j - carpetLen + 1],  # 铺地毯, 用上一轮的值
                    dp[j] + (1 if floor[j] == "1" else 0),  # 不铺
                )
            pre = dp
        return pre[n]

    # time O(numCarpets * n), space O(numCarpets * n)
    def minimumWhiteTilesDPWithGrid(self, floor: str, numCarpets: int, carpetLen: int) -> int:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示用 i 块地毯覆盖 floor[0..j] 后的最少白色瓷砖数.
        # dp[0] 初始化为白色瓷砖前缀和 (无地毯时直接计数).
        n = len(floor)
        dp = [[0] * (n + 1) for _ in range(numCarpets + 1)]
        for i in range(n):
            dp[0][i + 1] = dp[0][i] + (1 if floor[i] == "1" else 0)
        for i in range(numCarpets):
            for j in range(n):
                if j < (i + 1) * carpetLen:
                    continue
                dp[i + 1][j + 1] = min(
                    dp[i][j - carpetLen + 1],  # 铺地毯, 引用上一轮
                    dp[i + 1][j] + (1 if floor[j] == "1" else 0),  # 不铺
                )
        return dp[numCarpets][n]

    # time O(numCarpets * n), space O(numCarpets * n)
    def minimumWhiteTilesDFSWithMemorization(
        self, floor: str, numCarpets: int, carpetLen: int
    ) -> int:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j): 用 i+1 块地毯覆盖 floor[0..j] 后的最少白色瓷砖数.
        n = len(floor)

        @cache
        def dfs(i: int, j: int) -> int:
            if j < (i + 1) * carpetLen:
                return 0  # 地毯足够覆盖所有位置
            if i == -1:
                # 无地毯可用, 直接累加白色瓷砖数
                return 0 if j == -1 else dfs(i, j - 1) + (1 if floor[j] == "1" else 0)
            return min(
                dfs(i - 1, j - carpetLen),  # 铺地毯覆盖 floor[j-carpetLen+1..j]
                dfs(i, j - 1) + (1 if floor[j] == "1" else 0),  # 不铺
            )

        return dfs(numCarpets - 1, n - 1)
