# 956. Tallest Billboard
# https://leetcode.com/problems/tallest-billboard/
# Difficulty: Hard

from collections import defaultdict
from functools import cache


class Solution:
    # time O(n * s), space O(s)
    def tallestBillboard(self, rods: list[int]) -> int:
        # 空间优化版 DP
        n = len(rods)

        pre = defaultdict(lambda: -(10**5))
        pre[0] = 0
        for i in range(n):
            dp = defaultdict(lambda: -(10**5))
            for j, v in pre.items():
                dp[j - rods[i]] = max(dp[j - rods[i]], v + rods[i])
                dp[j] = max(dp[j], v)
                dp[j + rods[i]] = max(dp[j + rods[i]], v)
            pre = dp

        return pre[0]

    def tallestBillboardDPWithGridOptimized(self, rods: list[int]) -> int:
        n = len(rods)

        dp = [defaultdict(lambda: -(10**5)) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(n):
            # 优化: 只处理当前 dp[i] 中的 j 而不是 -s 到 s 的所有 j
            for j, v in dp[i].items():
                dp[i + 1][j - rods[i]] = max(dp[i + 1][j - rods[i]], v + rods[i])
                dp[i + 1][j] = max(dp[i + 1][j], v)
                dp[i + 1][j + rods[i]] = max(dp[i + 1][j + rods[i]], v)

        return dp[n][0]

    # time O(n * s), space O(n * s)
    def tallestBillboardDPWithGrid(self, rods: list[int]) -> int:
        n = len(rods)
        s = sum(rods) + 1

        # 注意 j 的范围是 -s 到 s 但是 Python 不支持负数索引所以用 defaultdict 来处理负数索引的情况
        dp = [defaultdict(lambda: -(10**5)) for _ in range(n + 1)]
        dp[0][0] = 0
        for i in range(n):
            for j in range(-s, s):
                dp[i + 1][j] = max(dp[i][j + rods[i]] + rods[i], dp[i][j], dp[i][j - rods[i]])

        return dp[n][0]

    # time O(n * s), space O(s)
    def tallestBillboardDFSWithMemorization(self, rods: list[int]) -> int:
        n = len(rods)

        @cache
        def dfs(i: int, s: int) -> int:
            if i == -1:
                # 如果 s == 0 说明两边一样高，返回 0 代表当前没有差距了；
                # 如果 s != 0 说明两边不一样高，返回一个很大的负数代表这个方案不可行。
                return 0 if s == 0 else -(10**4)
            return max(
                # 注意只需要统计放在左边的长度所以要加上 rods[i]
                dfs(i - 1, rods[i] + s) + rods[i],  # 选择放在左边
                dfs(i - 1, s),  # 选择不放
                dfs(i - 1, s - rods[i]),  # 选择放在右边
            )

        return dfs(n - 1, 0)
