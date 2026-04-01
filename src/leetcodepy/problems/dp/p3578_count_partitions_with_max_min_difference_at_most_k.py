# 3578. Count Partitions With Max-Min Difference at Most K
# https://leetcode.com/problems/count-partitions-with-max-min-difference-at-most-k/
# Difficulty: Medium


from collections import deque
from functools import cache
from math import inf


class Solution:
    # time O(n), space O(n)
    def countPartitions(self, nums: list[int], k: int) -> int:
        # 单调队列 + 前缀和优化 DP
        # 随着 j 往左移, [j, i] 的 max-min 只增不减, 存在一个左边界 left
        # 所有 j >= left 都合法, dp[i+1] = sum(dp[left] ... dp[i])
        # 用前缀和 O(1) 求区间和, 单调队列 O(1) 维护滑动窗口 max/min
        n, mod = len(nums), 10**9 + 7
        dp = [1] + [0] * n
        # pre 是 dp 的前缀和:
        # pre[0] = 0
        # pre[1] = dp[0]
        # pre[i+1] = dp[0] + dp[1] + ... + dp[i]
        pre = [0] * (n + 2)
        pre[1] = 1
        max_q: deque[int] = deque()  # 单调递减队列, 维护窗口最大值
        min_q: deque[int] = deque()  # 单调递增队列, 维护窗口最小值
        left = 0
        for i in range(n):
            while max_q and nums[max_q[-1]] <= nums[i]:
                max_q.pop()
            max_q.append(i)
            while min_q and nums[min_q[-1]] >= nums[i]:
                min_q.pop()
            min_q.append(i)
            # 收缩左边界直到 max - min <= k - 单调站维护窗口的最大最
            # 小值和收缩，实质上就是 dfs 里面固定右端点 i 找左端点 j
            while nums[max_q[0]] - nums[min_q[0]] > k:
                left += 1
                if max_q[0] < left:
                    max_q.popleft()
                if min_q[0] < left:
                    min_q.popleft()
            # DFS 里的内层循环: res += dp[j] for j in range(left, i+1)
            # 即 dp[left] + dp[left+1] + ... + dp[i]
            # 用前缀和替代:
            #   pre[i+1]  = dp[0] + dp[1] + ... + dp[i]
            #   pre[left] = dp[0] + dp[1] + ... + dp[left-1]
            #   pre[i+1] - pre[left] = dp[left] + ... + dp[i]
            # 正确性: 从左到右遍历, 每轮结束时算出 pre[i+2]
            #   所以算 dp[i+1] 时, pre[0] 到 pre[i+1] 都已就绪
            #   left <= i, 所以 pre[left] 也一定已算好
            dp[i + 1] = (pre[i + 1] - pre[left]) % mod
            # 算出 dp[i+1] 后追加到前缀和, 供下一轮 i+1 使用
            pre[i + 2] = (pre[i + 1] + dp[i + 1]) % mod
        return dp[n]

    # time O(n^2), space O(n) - 超时
    def countPartitionsDFSWithMemorization(self, nums: list[int], k: int) -> int:
        # 记忆化搜索: 从 i 往前枚举最后一段, 维护区间 max/min
        # dfs(i): nums[0..i] 的合法划分方案数
        n, mod = len(nums), 10**9 + 7

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 1
            res, min_num, max_num = 0, inf, -inf
            for j in range(i, -1, -1):
                min_num = min(min_num, nums[j])
                max_num = max(max_num, nums[j])
                if max_num - min_num > k:
                    break  # 再往左只会更大, 提前退出
                res = (res + dfs(j - 1)) % mod
            return res

        return dfs(n - 1)
