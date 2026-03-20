# 300. Longest Increasing Subsequence
# https://leetcode.com/problems/longest-increasing-subsequence/
# Difficulty: Medium


from bisect import bisect_left
from functools import cache


class BIT:
    """树状数组(Binary Indexed Tree), 这里用 max 代替求和,
    支持单点更新最大值和前缀最大值查询"""

    __slots__ = "tree"

    def __init__(self, n: int):
        self.tree = [0] * (n + 1)

    def update(self, index: int, val: int) -> None:
        # 把下标 index 的值更新为 max(原值, val)
        while index < len(self.tree):
            self.tree[index] = max(self.tree[index], val)
            index += index & -index  # 往上走, 更新管辖该位置的节点

    def pre(self, index: int) -> int:
        # 查询 [1, index] 范围内的最大值
        res = 0
        while index > 0:
            res = max(res, self.tree[index])
            index -= index & -index  # 往下走, 累计各段最大值
        return res


class Solution:
    # time O(n * log(n)), space O(n)
    def lengthOfLISBIT(self, nums: list[int]) -> int:
        # 树状数组解法: tree[v] 表示以值 v 结尾的 LIS 最大长度
        # 对于每个 nums[i], 查询所有 < nums[i] 的值中 LIS 的最大长度, 然后 +1
        #
        # 示例: nums = [10, 9, 2, 5, 3, 7, 101, 18]
        # 离散化: arr = [2, 3, 5, 7, 9, 10, 18, 101] (排序去重)
        #   nums[i]=10  → idx=6, pre(5)=0, 更新 tree[6]=1
        #   nums[i]=9   → idx=5, pre(4)=0, 更新 tree[5]=1
        #   nums[i]=2   → idx=1, pre(0)=0, 更新 tree[1]=1
        #   nums[i]=5   → idx=3, pre(2)=1, 更新 tree[3]=2  (2→5)
        #   nums[i]=3   → idx=2, pre(1)=1, 更新 tree[2]=2  (2→3)
        #   nums[i]=7   → idx=4, pre(3)=2, 更新 tree[4]=3  (2→3→7)
        #   nums[i]=101 → idx=8, pre(7)=3, 更新 tree[8]=4  (2→3→7→101)
        #   nums[i]=18  → idx=7, pre(6)=3, 更新 tree[7]=4  (2→3→7→18)
        # 答案: 4
        res = 0
        n = len(nums)
        # 离散化: 将值映射到 [1, m] 的连续整数, 压缩树状数组大小
        arr = sorted(set(nums))
        m = len(arr)
        bit = BIT(m)
        for i in range(n):
            # bisect_left(arr, nums[i]+1) 找到第一个 >= nums[i]+1 的位置
            # 即 <= nums[i] 的元素个数, 也就是 nums[i] 离散化后的下标
            idx = bisect_left(arr, nums[i] + 1)
            # 查询所有严格小于 nums[i] 的值中, LIS 的最大长度
            l = bit.pre(idx - 1)
            res = max(res, l + 1)
            # 更新: 以 nums[i] 结尾的 LIS 长度为 l+1
            bit.update(idx, l + 1)
        return res

    # time O(n * log(n)), space O(n)
    def lengthOfLISGreedy(self, nums: list[int]) -> int:
        # 贪心 + 二分: 维护一个有序数组 lcs, lcs[i] 表示长度为 i+1 的递增子序列的
        # 最小末尾元素
        # lcs 的长度就是最长递增子序列的长度
        # 注意: lcs 不是实际的 LIS, 只是用来维护最小末尾元素
        #
        # 示例: nums = [10, 9, 2, 5, 3, 7, 101, 18]
        #   10  → lcs = [10]           bisect_left=0, 替换 → [10]
        #   9   → lcs = [9]            bisect_left=0, 替换 → [9]
        #   2   → lcs = [2]            bisect_left=0, 替换 → [2]
        #   5   → lcs = [2, 5]         bisect_left=1, 追加 → [2, 5]
        #   3   → lcs = [2, 3]         bisect_left=1, 替换 → [2, 3]
        #   7   → lcs = [2, 3, 7]      bisect_left=2, 追加 → [2, 3, 7]
        #   101 → lcs = [2, 3, 7, 101] bisect_left=3, 追加 → [2, 3, 7, 101]
        #   18  → lcs = [2, 3, 7, 18]  bisect_left=3, 替换 → [2, 3, 7, 18]
        # 答案: len(lcs) = 4
        n = len(nums)
        lcs = []
        for i in range(n):
            # 二分找 nums[i] 在 lcs 中的插入位置(第一个 >= nums[i] 的位置)
            j = bisect_left(lcs, nums[i])
            if j == len(lcs):
                # nums[i] 比 lcs 中所有元素都大, 可以延长递增子序列
                lcs.append(nums[i])
            else:
                # 用更小的 nums[i] 替换 lcs[j], 为后续元素留更多空间
                lcs[j] = nums[i]
        return len(lcs)

    # time O(n^2), space O(n)
    def lengthOfLISDP(self, nums: list[int]) -> int:
        # 把记忆化搜索翻译成 DP
        n = len(nums)
        dp = [0] * n
        for i in range(n):
            m = 0
            for j in range(i):
                if nums[i] > nums[j]:
                    m = max(m, dp[j])
            dp[i] = m + 1
        res = 0
        for i in range(n):
            res = max(res, dp[i])
        return res

    # time O(n^2), space O(n)
    def lengthOfLISDFSWithMemorization(self, nums: list[int]) -> int:
        # 记忆化搜索
        n = len(nums)

        @cache
        def dfs(i: int) -> int:
            res = 0
            # 继续往前找比 nums[i] 小的数来构造最长递增子序列
            for j in range(i):
                if nums[i] > nums[j]:
                    res = max(res, dfs(j))
            return res + 1

        lcs = 0
        for i in range(n):
            lcs = max(lcs, dfs(i))
        return lcs
