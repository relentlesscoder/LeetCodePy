# 2052. Minimum Cost to Separate Sentence Into Rows
# https://leetcode.com/problems/minimum-cost-to-separate-sentence-into-rows/
# Difficulty: Medium


from functools import cache
from math import inf


class Solution:
    # time O(m * k), space O(m)
    def minimumCostDP(self, sentence: str, k: int) -> int:
        # 将句子分行, 每行长度 <= k, 代价 = (k - 行长)^2, 最后一行免费
        # 先提取每个单词的长度
        n, cnt = len(sentence), 0
        nums: list[int] = []
        for i in range(n + 1):
            if i == n or sentence[i] == " ":
                nums.append(cnt)
                cnt = 0
                continue
            cnt += 1
        # dp[i]: 从第 i 个单词开始的最小总代价
        # 从 i 往右枚举同一行的单词 nums[i..j], 累加长度(含空格)直到超出 k
        m = len(nums)
        dp = [inf] * (m + 1)
        dp[m] = 0  # 没有单词了, 代价为 0
        for i in range(m - 1, -1, -1):
            res, length = inf, 0
            for j in range(i, m):
                space = 0 if j == i else 1  # 第一个单词前无空格
                if length + space + nums[j] > k:
                    break
                length += space + nums[j]
                # 最后一行免费(代价 0), 否则代价 = (k - 行长)^2
                cost = 0 if j + 1 == m else (k - length) * (k - length)
                res = min(res, cost + dp[j + 1])
            dp[i] = res
        return dp[0]

    # time O(m * k), space O(m)
    def minimumCostDFSWithMemorization(self, sentence: str, k: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): 从第 i 个单词开始的最小总代价
        n, cnt = len(sentence), 0
        nums: list[int] = []
        for i in range(n + 1):
            if i == n or sentence[i] == " ":
                nums.append(cnt)
                cnt = 0
                continue
            cnt += 1
        m = len(nums)

        @cache
        def dfs(i: int) -> int:
            if i == m:
                return 0
            res, length = inf, 0
            for j in range(i, m):
                space = 0 if j == i else 1
                if length + space + nums[j] > k:
                    break
                length += space + nums[j]
                cost = 0 if j + 1 == m else (k - length) * (k - length)
                res = min(res, cost + dfs(j + 1))
            return res

        return dfs(0)
