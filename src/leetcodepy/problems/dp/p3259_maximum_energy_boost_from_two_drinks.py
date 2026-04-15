# 3259. Maximum Energy Boost From Two Drinks
# https://leetcode.com/problems/maximum-energy-boost-from-two-drinks/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def maxEnergyBoostDP(self, energyDrinkA: list[int], energyDrinkB: list[int]) -> int:
        # 状态机 DP, 滚动变量. 每小时选一种饮料, 切换需跳过一小时.
        # 与 p0309 (股票冷却) 结构类似: 切换饮料 = 卖出后冷却再买入.
        #
        #         切换 (跳过 1 小时)
        #       ┌────────────────────┐
        #       │                    ▼
        #   ┌───┐ ┌───┐        ┌───┐ ┌───┐
        #   │   └▶│ A │        │ B │◀┘   │
        #   └────◀┘   │        │   └▶────┘
        #   继续  └───┘        └───┘  继续
        #       ▲                    │
        #       └────────────────────┘
        #         切换 (跳过 1 小时)
        #
        # d1[0/1]: 上一小时选 A/B 的最大能量
        # d0[0/1]: 前一小时选 A/B 的最大能量 (切换时跳过冷却用)
        n = len(energyDrinkA)
        d0, d1 = [0, 0], [energyDrinkA[0], energyDrinkB[0]]
        for i in range(1, n, 1):
            c = [0, 0]
            c[0] = max(d1[0], d0[1]) + energyDrinkA[i]  # 继续喝 A or 从 B 切换 (跳 1 小时)
            c[1] = max(d1[1], d0[0]) + energyDrinkB[i]  # 继续喝 B or 从 A 切换 (跳 1 小时)
            d0 = d1  # 滚动: 今天变成明天的"前天"
            d1 = c
        return max(d1[0], d1[1])

    # time O(n), space O(n)
    def maxEnergyBoostDPWithGrid(self, energyDrinkA: list[int], energyDrinkB: list[int]) -> int:
        # 数组 DP, 显式保存每小时状态, 便于理解.
        # dp[i+1][0]: 第 i 小时选 A 的最大能量
        # dp[i+1][1]: 第 i 小时选 B 的最大能量
        # 切换时引用 dp[i-1] (前两小时), 跳过冷却, 类似 p0309.
        n = len(energyDrinkA)
        dp = [[0, 0] for _ in range(n + 1)]
        dp[1] = [energyDrinkA[0], energyDrinkB[0]]
        for i in range(1, n, 1):
            dp[i + 1][0] = max(dp[i][0], dp[i - 1][1]) + energyDrinkA[i]  # 继续 A or 从 B 切换
            dp[i + 1][1] = max(dp[i][1], dp[i - 1][0]) + energyDrinkB[i]  # 继续 B or 从 A 切换
        return max(dp[n][0], dp[n][1])

    # time O(n), space O(n)
    def maxEnergyBoostDFSWithMemorization(
        self, energyDrinkA: list[int], energyDrinkB: list[int]
    ) -> int:
        # 记忆化搜索 (自顶向下), 与数组 DP 等价.
        # dfs(i, j): 考虑前 i+1 小时, 第 i 小时选饮料 j (0=A, 1=B) 的最大能量.
        # 切换时递归到 i-2 (跳过冷却), 不切换递归到 i-1.
        n = len(energyDrinkA)

        @cache
        def dfs(i: int, j: int) -> int:
            if i < 0:
                return 0
            if j == 0:
                # 选 A: 上一小时也选 A (i-1) or 从 B 切换 (跳过 i-1, 用 i-2)
                return max(dfs(i - 1, 0), dfs(i - 2, 1)) + energyDrinkA[i]
            # 选 B: 上一小时也选 B (i-1) or 从 A 切换 (跳过 i-1, 用 i-2)
            return max(dfs(i - 1, 1), dfs(i - 2, 0)) + energyDrinkB[i]

        return max(dfs(n - 1, 0), dfs(n - 1, 1))
