# 3610. Minimum Number of Primes to Sum to Target
# https://leetcode.cn/problems/minimum-number-of-primes-to-sum-to-target/
# Difficulty: Medium


from functools import cache

MAX = 1_000

# 预处理出前 1000 个质数
NON_PRIME = [False] * (MAX + 1)
for _i in range(2, MAX + 1):  # 埃氏筛
    if not NON_PRIME[_i]:
        for _j in range(_i, MAX // _i + 1):
            NON_PRIME[_i * _j] = True


# 获取前 m 个质数
def getPrimes(m: int) -> list[int]:
    primes = []
    i = 2
    while i <= MAX and len(primes) < m:
        if not NON_PRIME[i]:
            primes.append(i)
        i += 1
    return primes


class Solution:
    # time O(n * k), space O(n)
    def minNumberOfPrimes(self, n: int, m: int) -> int:
        # 空间优化版 DP
        nums = getPrimes(m)
        k = len(nums)
        dp = [0] + [MAX] * (n + 1)
        for i in range(k):
            for s in range(1, n + 1):
                if nums[i] <= s:
                    dp[s] = min(dp[s], 1 + dp[s - nums[i]])
        return dp[n] if dp[n] < MAX else -1

    # time O(n * k), space O(n * k)
    def minNumberOfPrimesDPWithGrid(self, n: int, m: int) -> int:
        # 将记忆化搜索翻译成 DP
        nums = getPrimes(m)
        k = len(nums)
        dp = [[0] + [MAX] * (n + 1) for _ in range(k + 1)]
        for i in range(k):
            for s in range(1, n + 1):
                if nums[i] > s:
                    dp[i + 1][s] = dp[i][s]
                else:
                    dp[i + 1][s] = min(dp[i][s], 1 + dp[i + 1][s - nums[i]])
        return dp[k][n] if dp[k][n] < MAX else -1

    # time O(n * k), space O(n * k)
    def minNumberOfPrimesDFSWithMemorization(self, n: int, m: int) -> int:
        nums = getPrimes(m)
        k = len(nums)

        @cache
        def dfs(i: int, s: int) -> int:
            if s == 0:  # 说明之前选的质数的和正好凑成了目标值 n, 这是一种合法的方案
                return 0
            if i == -1:  # 没有质数了, 说明之前选的质数的和没有凑成目标值 n, 这不是一种合法的方案
                return MAX
            if nums[i] > s:  # 如果当前质数的值超过了剩余的目标值, 那么只能不选这个质数
                return dfs(i - 1, s)
            else:  # 否则可以选择不选这个质数, 或者选这个质数
                return min(dfs(i - 1, s), 1 + dfs(i, s - nums[i]))

        res = dfs(k - 1, n)
        return res if res < MAX else -1
