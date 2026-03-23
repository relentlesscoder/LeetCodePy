# 673. Number of Longest Increasing Subsequence
# https://leetcode.com/problems/number-of-longest-increasing-subsequence/
# Difficulty: Medium


from bisect import bisect_left


class Solution:
    # time O(n * log(n)), space O(n)
    def findNumberOfLISBinaryIndexedTree(self, nums: list[int]) -> int:
        # BIT 维护 (最大长度, 方案数), 以离散化后的值为下标
        # 按原数组顺序逐个处理, 查询值域 [1, idx-1] 的前缀最大长度和对应方案数
        sorted_set = sorted(set(nums))
        m = len(sorted_set)
        bit = BIT(m)
        max_lis = 0
        total = 0
        for num in nums:
            # 离散化: 映射到 [1, m]
            idx = bisect_left(sorted_set, num) + 1
            # 查前缀 [1, idx-1]: 值严格小于 num 的最大 LIS 长度和方案数
            prev_len, prev_cnt = bit.query(idx - 1)
            cur_len = prev_len + 1
            cur_cnt = max(prev_cnt, 1)  # 没有前驱时方案数为 1
            bit.update(idx, cur_len, cur_cnt)
            if cur_len > max_lis:
                max_lis = cur_len
                total = cur_cnt
            elif cur_len == max_lis:
                total += cur_cnt
        return total

    # time O(n * log(n)), space O(n)
    def findNumberOfLISGreedy(self, nums: list[int]) -> int:
        # 贪心 + 前缀和: 类似 patience sorting
        # d[k] 存 LIS 长度为 k+1 的所有末尾值和前缀方案数
        # 每堆中值非递增(新加入的更小), 前缀方案数递增
        # tails[k] = d[k] 最小值(最后一个), 用于外层二分查找
        d: list[list[tuple[int, int]]] = []
        tails: list[int] = []
        for num in nums:
            # 外层二分: 找第一个 tails[k] >= num 的堆
            k = bisect_left(tails, num)
            # 计算方案数
            if k == 0:
                cnt = 1
            else:
                # 在 d[k-1] 中找值 < num 的条目(非递增序列的尾部)
                # 二分找第一个 < num 的位置
                prev = d[k - 1]
                lo, hi = 0, len(prev)
                while lo < hi:
                    mid = (lo + hi) // 2
                    if prev[mid][0] >= num:
                        lo = mid + 1
                    else:
                        hi = mid
                # lo..end 的值都 < num, 用前缀和求这些条目的总方案数
                cnt = prev[-1][1] - (prev[lo - 1][1] if lo > 0 else 0)
            # 加入堆 k
            if k == len(d):
                d.append([])
                tails.append(num)
            else:
                tails[k] = num
            prefix = cnt + (d[k][-1][1] if d[k] else 0)
            d[k].append((num, prefix))
        return d[-1][-1][1]

    # time O(n^2), space O(n)
    def findNumberOfLISDP(self, nums: list[int]) -> int:
        # dp[i]: 以 nums[i] 结尾的 LIS 长度
        # cnt[i]: 以 nums[i] 结尾的 LIS 方案数
        n = len(nums)
        dp = [1] * n
        cnt = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    if dp[j] + 1 > dp[i]:
                        # 找到更长的 LIS, 重置方案数
                        dp[i] = dp[j] + 1
                        cnt[i] = cnt[j]
                    elif dp[j] + 1 == dp[i]:
                        # 同样长度, 累加方案数
                        cnt[i] += cnt[j]
        max_len = max(dp)
        return sum(cnt[i] for i in range(n) if dp[i] == max_len)


class BIT:
    __slots__ = ("count", "length", "n")

    def __init__(self, n: int):
        self.n = n
        self.length = [0] * (n + 1)  # 每个节点存该管辖区间的最大 LIS 长度
        self.count = [0] * (n + 1)  # 对应的方案数

    def update(self, i: int, length: int, c: int) -> None:
        while i <= self.n:
            if length > self.length[i]:
                self.length[i] = length
                self.count[i] = c
            elif length == self.length[i]:
                self.count[i] += c
            i += i & -i

    def query(self, i: int) -> tuple[int, int]:
        max_l, cnt = 0, 0
        while i > 0:
            if self.length[i] > max_l:
                max_l = self.length[i]
                cnt = self.count[i]
            elif self.length[i] == max_l:
                cnt += self.count[i]
            i -= i & -i
        return max_l, cnt
