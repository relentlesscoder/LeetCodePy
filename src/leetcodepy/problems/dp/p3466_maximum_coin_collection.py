# 3466. Maximum Coin Collection
# https://leetcode.com/problems/maximum-coin-collection/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(n)
    def maxCoins(self, lane1: list[int], lane2: list[int]) -> int:
        # 子序列选取 DP. 从 lane1 进入高速, 最多切换 2 次, 求最大收益.
        # 选择起点和终点, 经过的每个位置必须收集 (可能为负).
        # dfs(i, j, k): 从位置 i 出发向右走, j 次切换剩余, 当前在 lane k.
        # 每个位置: 收集当前 lane 并选择继续/切换/结束.
        n = len(lane1)
        lanes = [lane1, lane2]

        @cache
        def dfs(i: int, j: int, k: int) -> int:
            if i == n:
                return 0  # 超出范围, 旅程已结束
            other = 1 - k
            res = max(
                lanes[k][i],  # 在此结束旅程
                lanes[k][i] + dfs(i + 1, j, k),  # 继续同一 lane
            )
            if j > 0:
                res = max(
                    res,
                    lanes[other][i],  # 切换并结束
                    lanes[other][i] + dfs(i + 1, j - 1, other),  # 切换并继续
                )
            return res

        # 枚举所有入口位置, 始终从 lane1 (k=0) 进入, 最多 2 次切换
        return max(dfs(i, 2, 0) for i in range(n))
