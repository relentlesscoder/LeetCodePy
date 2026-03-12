# 2189. Number of Ways to Build House of Cards
# https://leetcode.com/problems/number-of-ways-to-build-house-of-cards/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n * sqrt(n)), space O(sqrt(n))
    def houseOfCards(self, n: int) -> int:

        @cache
        def dfs(c: int, t: int) -> int:
            if c == 0:  # 0 张牌, 1 种搭法
                return 1
            res = 0
            # 搭 k 组三角需要 3k - 1 张牌, 如果剩余牌数 c 足够搭 k 组三角, 那么就递归地搭剩余的牌
            for k in range(1, t):
                cost = 3 * k - 1
                if cost > c:  # 如果剩余牌数 c 不够搭 k 组三角了, 后续的 k 都不够了, 可以直接剪枝了
                    break
                res += dfs(c - cost, k)
            return res

        # 拥有 n 张牌, 当前层最多只能搭 n//3 组三角
        return dfs(n, (n + 1) // 3 + 1)
