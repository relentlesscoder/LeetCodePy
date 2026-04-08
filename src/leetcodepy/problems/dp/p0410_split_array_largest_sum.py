# 410. Split Array Largest Sum
# https://leetcode.com/problems/split-array-largest-sum/
# Difficulty: Hard


from functools import cache
from math import inf


class Solution:
    # time O(n * log(sum - max)), space O(1)
    def splitArrayBinarySearch(self, nums: list[int], k: int) -> int:
        # 二分答案 + 贪心验证. 将数组分成 k 段, 最小化各段和的最大值.
        # 二分"最大子数组和"mid, 贪心检查能否在每段和 <= mid 下分成 <= k 段.
        # low = max(nums): 每个元素至少独占一段; high = sum(nums): 整个数组一段.
        low, high = max(nums), sum(nums)
        while low < high:
            mid, total, cnt = (low + high) // 2, 0, 1  # cnt=1 预先计入最后一段
            for x in nums:
                if total + x > mid:  # 当前段放不下 x, 切一刀开新段
                    total = 0
                    cnt += 1
                total += x
            if cnt <= k:  # 段数够少, mid 可行, 尝试更小的值
                high = mid
            else:
                low = mid + 1
        return low

    # time O(k * n^2), space O(n)
    def splitArrayDP(self, nums: list[int], k: int) -> int:
        # 1D 滚动数组 DP. 与 p3599 结构相同, 只是代价函数从 XOR 变为子数组和.
        # dp[j+1] 表示将 nums[0..j] 分成若干段时, 各段和最大值的最小值.
        # 每轮 i 对应"再增加一段", 枚举最后一段起点 x, 状态转移为:
        #   dp[j+1] = min(max(sum(nums[x..j]), dp[x]))  for x in [i, j]
        n = len(nums)
        dp = [0] + [inf] * n
        for i in range(k):
            for j in range(n - 1, i - 1, -1):  # 从右向左保证本轮只用上一轮的值
                res, total = inf, 0
                for x in range(j, i - 1, -1):  # 枚举最后一段起点, 同时累积区间和
                    total += nums[x]
                    if total >= res:  # 剪枝: 子数组和已不优于已知最优
                        continue
                    # max(当前段和, 前面段的最优 minimax) 取较小者
                    res = min(res, max(total, dp[x]))
                dp[j + 1] = res
        return dp[n]

    # time O(k * n^2), space O(k * n)
    def splitArrayDPWithGrid(self, nums: list[int], k: int) -> int:
        # 二维 DP, 显式保存每轮状态, 便于理解.
        # dp[i][j+1] 表示将 nums[0..j] 分成恰好 i+1 段时, 各段和最大值的最小值.
        n = len(nums)
        dp = [[0] + [inf] * n] + [[inf] * (n + 1) for _ in range(k)]
        for i in range(k):
            for j in range(n - 1, i - 1, -1):
                res, total = inf, 0
                for x in range(j, i - 1, -1):
                    total += nums[x]
                    if total >= res:
                        continue
                    # 引用上一轮 dp[i][x], 即前 x 个元素分成 i 段的最优值
                    res = min(res, max(total, dp[i][x]))
                dp[i + 1][j + 1] = res
        return dp[k][n]

    # time O(k * n^2), space O(k * n)
    def splitArrayDFSWithMemorization(self, nums: list[int], k: int) -> int:
        # 记忆化搜索 (自顶向下), 与二维 DP 等价.
        # dfs(i, j) 表示将 nums[0..j] 分成恰好 i+1 段时, 各段和最大值的最小值.
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            if i == -1:
                return 0 if j == -1 else inf  # 段数用完: 前缀也恰好为空则合法
            if j == -1:
                return inf  # 前缀已空但还需分段, 不合法
            res, total = inf, 0
            for x in range(j, i - 1, -1):  # 枚举最后一段起点 x
                total += nums[x]
                if total >= res:  # 剪枝
                    continue
                # max(最后一段和, 前面段的最优 minimax) 取较小者
                res = min(res, max(total, dfs(i - 1, x - 1)))
            return res

        return dfs(k - 1, n - 1)
