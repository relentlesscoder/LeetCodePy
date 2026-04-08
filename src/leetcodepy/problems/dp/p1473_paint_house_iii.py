# 1473. Paint House III
# https://leetcode.com/problems/paint-house-iii/
# Difficulty: Hard

from functools import cache
from math import inf


class Solution:
    # time O(m * target * n), space O(target * n)
    def minCostDPOptimized(
        self, houses: list[int], cost: list[list[int]], m: int, n: int, target: int
    ) -> int:
        # 滚动 DP + 最小/次小值优化.
        # 与 minCostDP 相同, 但预处理每行 dp[k-1] 的最小值和次小值,
        # 将枚举 c_prev 的 O(n) 降为 O(1), 总复杂度从 O(m*target*n^2) 降到 O(m*target*n).
        if target > m:
            return -1
        dp = [[inf] * (n + 1) for _ in range(target + 1)]
        dp[0][0] = 0
        for j in range(m):
            # 预处理每行 dp[k] 的最小值和次小值 (用于异色转移)
            # min1[k] = (最小值, 对应颜色), min2[k] = (次小值, 对应颜色)
            min1 = [(inf, -1)] * (target + 1)
            min2 = [(inf, -1)] * (target + 1)
            for k in range(target + 1):
                for c in range(n + 1):
                    if dp[k][c] < min1[k][0]:
                        min2[k] = min1[k]
                        min1[k] = (dp[k][c], c)
                    elif dp[k][c] < min2[k][0]:
                        min2[k] = (dp[k][c], c)
            new_dp = [[inf] * (n + 1) for _ in range(target + 1)]
            colors = [houses[j]] if houses[j] > 0 else range(1, n + 1)
            for color in colors:
                paint_cost = 0 if houses[j] > 0 else cost[j][color - 1]
                for k in range(target + 1):
                    # 同色: 街区数不变
                    val = dp[k][color] + paint_cost
                    if val < new_dp[k][color]:
                        new_dp[k][color] = val
                    # 异色: 新增街区, 用最小/次小值 O(1) 查询
                    if k > 0:
                        # 若 color 恰好是 dp[k-1] 的最小值颜色, 用次小值
                        best = min1[k - 1] if min1[k - 1][1] != color else min2[k - 1]
                        val = best[0] + paint_cost
                        if val < new_dp[k][color]:
                            new_dp[k][color] = val
            dp = new_dp
        res = min(dp[target][c] for c in range(1, n + 1))
        return -1 if res == inf else res

    # time O(m * target * n^2), space O(target * n)
    def minCostDP(
        self, houses: list[int], cost: list[list[int]], m: int, n: int, target: int
    ) -> int:
        # 从左到右 DP. dp[k][c] = 处理完当前房子后, 形成 k 个街区,
        # 最后一个房子颜色为 c 时的最小花费. c=0 表示还没有房子.
        if target > m:
            return -1
        dp = [[inf] * (n + 1) for _ in range(target + 1)]
        dp[0][0] = 0  # 初始: 0 个街区, 无颜色
        for j in range(m):
            new_dp = [[inf] * (n + 1) for _ in range(target + 1)]
            # 如果已涂色, 只能用该颜色; 否则尝试所有颜色
            colors = [houses[j]] if houses[j] > 0 else range(1, n + 1)
            for color in colors:
                paint_cost = 0 if houses[j] > 0 else cost[j][color - 1]
                for k in range(target + 1):
                    # 与前一个房子同色: 街区数不变
                    if dp[k][color] + paint_cost < new_dp[k][color]:
                        new_dp[k][color] = dp[k][color] + paint_cost
                    # 与前一个房子异色: 新增街区 (k-1 → k)
                    if k > 0:
                        for c_prev in range(n + 1):
                            if c_prev == color:
                                continue
                            val = dp[k - 1][c_prev] + paint_cost
                            if val < new_dp[k][color]:
                                new_dp[k][color] = val
            dp = new_dp
        res = min(dp[target][c] for c in range(1, n + 1))
        return -1 if res == inf else res

    # time O(m * target * n^2), space O(m * target * n)
    def minCostDPWithGrid(
        self, houses: list[int], cost: list[list[int]], m: int, n: int, target: int
    ) -> int:
        # 三维 DP, 直接从记忆化搜索翻译而来.
        # dfs(i, j, c) → dp[j+1][i+1][c]
        #   i: 剩余街区数-1 (-1..target-1) → dp 第二维 (0..target)
        #   j: 房子下标 (-1..m-1) → dp 第一维 (0..m)
        #   c: 右邻居颜色 (0..n) → dp 第三维 (0..n)
        # base case: dfs(i, -1, c) = 0 if i==-1 else inf
        #   → dp[0][0][c] = 0 for all c, dp[0][i][c] = inf for i > 0
        if target > m:
            return -1
        # dp[j+1][i+1][c]: 处理 houses[0..j], 还需 i+1 个街区, 右邻居颜色 c
        dp = [[[inf] * (n + 1) for _ in range(target + 1)] for _ in range(m + 1)]
        for c in range(n + 1):
            dp[0][0][c] = 0  # base: j==-1, i==-1 → 0
        # 从左到右填表 (对应 dfs 从 j 递归到 j-1)
        for j in range(m):
            for i in range(target + 1):
                for c in range(n + 1):
                    if c > 0 and houses[j] == c:
                        # 与右邻居同色, 不新增街区
                        dp[j + 1][i][c] = dp[j][i][c]
                    elif houses[j] > 0:
                        # 已涂色且与右邻居不同, 新增街区
                        if i > 0:
                            dp[j + 1][i][c] = dp[j][i - 1][houses[j]]
                    else:
                        # 未涂色, 尝试所有颜色
                        res = inf
                        for x in range(n):
                            if x + 1 == c:
                                # 同色, 不新增街区
                                val = cost[j][x] + dp[j][i][c]
                            elif i > 0:
                                # 异色, 新增街区
                                val = cost[j][x] + dp[j][i - 1][x + 1]
                            else:
                                continue
                            res = min(res, val)
                        dp[j + 1][i][c] = res
        # 答案: dfs(target-1, m-1, 0) → dp[m][target][0]
        res = dp[m][target][0]
        return -1 if res == inf else res

    # time O(m * target * n^2), space O(m * target * n)
    def minCostDFSWithMemorization(
        self, houses: list[int], cost: list[list[int]], m: int, n: int, target: int
    ) -> int:
        # 记忆化搜索, 从右往左处理房子.
        # dfs(i, j, c): 处理 houses[0..j], 还需形成 i+1 个街区,
        #   houses[j] 右边的颜色为 c (0 表示无右邻居).
        # 街区由颜色变化决定: 与右邻居同色不新增, 异色则新增.
        # 注意: i == -1 时不能直接返回 inf, 因为剩余房子可能
        #   与右邻居同色(属于同一街区), 不需要额外街区额度.
        if target > m:
            return -1

        @cache
        def dfs(i: int, j: int, c: int) -> int:
            if j == -1:
                return 0 if i == -1 else inf  # 所有房子处理完, 街区恰好用完才合法
            if c > 0 and houses[j] == c:
                # 与右邻居同色, 属于同一街区, 不消耗 i
                return dfs(i, j - 1, c)
            elif houses[j] > 0:
                # 已涂色且与右邻居不同, 新增街区, 需要 i >= 0
                return dfs(i - 1, j - 1, houses[j]) if i >= 0 else inf
            # 未涂色, 枚举所有可选颜色
            res = inf
            for x in range(n - 1, -1, -1):
                if x + 1 == c:
                    # 涂成与右邻居同色, 不新增街区
                    res = min(res, cost[j][x] + dfs(i, j - 1, c))
                elif i >= 0:
                    # 涂成不同色, 新增街区
                    res = min(res, cost[j][x] + dfs(i - 1, j - 1, x + 1))
            return res

        min_cost = dfs(target - 1, m - 1, 0)
        return -1 if min_cost == inf else min_cost
