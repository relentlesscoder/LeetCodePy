# 2464. Minimum Subarrays in a Valid Split
# https://leetcode.com/problems/minimum-subarrays-in-a-valid-split/
# Difficulty: Medium


from functools import cache
from math import inf, isqrt


class Solution:
    # time O(n * sqrt(max)), space O(n + max), max = max(nums)
    def validSubarraySplitDPPrimeFactorization(self, nums: list[int]) -> int:
        # 质因数分解优化: 合法子数组要求首尾 gcd > 1, 即共享某个质因数
        # factor_map[f]: 拥有质因数 f 的所有位置中, 最小的 dp 值
        # 对每个 nums[i], 枚举其质因数, 查 factor_map 找最优分割点
        # 避免了内层遍历所有 j, 改为只枚举 O(sqrt(nums[i])) 个质因数
        n, mx = len(nums), 10**4
        dp = [0] * (n + 1)
        factor_map: dict[int, float] = {}
        for i in range(n):
            factors = self.prime_factors(nums[i])
            # 先更新 factor_map: 位置 i 可以作为未来的分割点
            for f in factors:
                factor_map[f] = min(factor_map.get(f, inf), dp[i])
            # 查 factor_map: 找与 nums[i] 共享质因数的最优分割点
            res = mx
            for f in factors:
                res = min(res, 1 + factor_map.get(f, 0))
            dp[i + 1] = res

        return -1 if dp[n] > n else dp[n]

    # time O(n^2 * log(max)), space O(n)
    def validSubarraySplitDP(self, nums: list[int]) -> int:
        # 合法分割: 每个子数组首尾元素的 gcd > 1
        # dp[i+1]: nums[0..i] 的最少子数组数
        # 从 i 往前枚举 j, 检查 gcd(nums[i], nums[j]) > 1
        n, mx = len(nums), 10**4
        dp = [0] * (n + 1)
        for i in range(n):
            res = mx
            for j in range(i, -1, -1):
                if self.gcd(nums[i], nums[j]) > 1:
                    res = min(res, 1 + dp[j])
            dp[i + 1] = res

        return -1 if dp[n] > n else dp[n]

    # time O(n^2 * log(max)), space O(n)
    def validSubarraySplitDFSWithMemorization(self, nums: list[int]) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): nums[0..i] 的最少子数组数
        n, mx = len(nums), 10**4

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            res = mx
            for j in range(i, -1, -1):
                if self.gcd(nums[i], nums[j]) > 1:
                    res = min(res, 1 + dfs(j - 1))
            return res

        partition = dfs(n - 1)
        return -1 if partition > n else partition

    def prime_factors(self, x: int) -> list[int]:
        # 返回 x 的所有质因数 (去重)
        res: list[int] = []
        for i in range(2, isqrt(x) + 1, 1):
            if x % i == 0:
                res.append(i)
                while x % i == 0:
                    x //= i  # 整除, 跳过重复因子
        if x > 1:
            res.append(x)  # 剩余的大质因数
        return res

    def gcd(self, a: int, b: int) -> int:
        while a != 0:
            temp = a
            a = b % a
            b = temp
        return b
