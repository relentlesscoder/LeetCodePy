# 1105. Filling Bookcase Shelves
# https://leetcode.com/problems/filling-bookcase-shelves/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(n * w), space O(n)
    def minHeightShelvesDP(self, books: list[list[int]], shelfWidth: int) -> int:
        # 按顺序摆书到书架上, 每层宽度 <= shelfWidth, 层高 = 该层最高的书
        # dp[i+1]: 摆完前 i+1 本书的最小总高度
        # 从 i 往前枚举同一层的书 books[j..i], 累加宽度直到超出
        # 该层高度 = max(books[j..i] 的高度), 加上前面的 dp[j]
        n = len(books)
        dp = [0] * (n + 1)
        for i in range(n):
            res, total_width, max_height = inf, 0, 0
            for j in range(i, -1, -1):
                total_width += books[j][0]
                if total_width > shelfWidth:
                    break  # 宽度超出, 不能再往前放
                max_height = max(max_height, books[j][1])
                res = min(res, max_height + dp[j])
            dp[i + 1] = res
        return dp[n]

    # time O(n * w), space O(n)
    def minHeightShelvesDFSWithMemorization(self, books: list[list[int]], shelfWidth: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): 摆完前 i+1 本书的最小总高度
        n = len(books)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            res, total_width, max_height = inf, 0, 0
            for j in range(i, -1, -1):
                total_width += books[j][0]
                if total_width > shelfWidth:
                    break
                max_height = max(max_height, books[j][1])
                res = min(res, max_height + dfs(j - 1))
            return res

        return dfs(n - 1)
