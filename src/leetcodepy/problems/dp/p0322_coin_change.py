# 322. Coin Change
# https://leetcode.com/problems/coin-change/
# Difficulty: Medium


from cmath import inf
from functools import cache


class Solution:
    # time O(n * a), space O(a)
    def coinChange(self, coins: list[int], amount: int) -> int:
        # 空间优化版 DP
        n = len(coins)
        dp = [0] + [inf] * (amount)
        for i in range(n):
            for a in range(amount + 1):
                if a >= coins[i]:
                    dp[a] = min(dp[a], 1 + dp[a - coins[i]])
        return -1 if dp[amount] == inf else dp[amount]

    # time O(n * a), space O(n * a)
    def coinChange(self, coins: list[int], amount: int) -> int:
        # 将记忆化搜索翻译成 DP
        n = len(coins)
        dp = [[0] + [inf] * (amount)] + [[0] * (amount + 1) for _ in range(n)]
        for i in range(n):
            for a in range(
                amount + 1
            ):  # 注意这里 a 从小到大遍历, 因为 dp[i + 1][a] 依赖于 dp[i + 1][a - coins[i]]
                if a < coins[i]:
                    dp[i + 1][a] = dp[i][a]
                else:
                    dp[i + 1][a] = min(dp[i][a], 1 + dp[i + 1][a - coins[i]])
        return -1 if dp[n][amount] == inf else dp[n][amount]

    # time O(n * a), space O(n * a)
    def coinChangeDFSWithMemorization(self, coins: list[int], amount: int) -> int:
        # 记忆化搜索
        n = len(coins)
        coins.sort(reverse=True)  # 优化: 先将硬币按面额从大到小排序, 这样在搜索过程中就能尽早剪枝了

        @cache
        def dfs(i: int, a: int) -> int:
            # 没有硬币了或者当前硬币的面额超过了剩余金额, 两种情况:
            #   如果金额也正好是 0, 那么说明之前选的硬币的金额正好凑成了目标金额, 这是一种合法的方案;
            #   如果金额不为 0, 那么说明之前选的硬币的金额没有凑成目标金额, 这不是一种合法的方案。
            if i == -1 or a < coins[i]:
                return 0 if a == 0 else inf
            # 否则可以选择不选这个硬币, 或者选这个硬币
            return min(dfs(i - 1, a), 1 + dfs(i, a - coins[i]))

        res = dfs(n - 1, amount)
        return -1 if res == inf else res
