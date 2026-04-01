# 2547. Minimum Cost to Split an Array
# https://leetcode.com/problems/minimum-cost-to-split-an-array/
# Difficulty: Hard


from functools import cache
from math import inf


class SegmentTree:
    __slots__ = ("length", "mark", "tree")

    def __init__(self, n: int):
        self.length = n
        size = 2 << n.bit_length()
        self.tree = [0] * size
        self.mark = [0] * size

    def query(self, start: int, end: int) -> int:
        return self._query(1, 1, self.length, start, end)

    def update(self, start: int, end: int, val: int) -> None:
        self._update(1, 1, self.length, start, end, val)

    def _query(self, node: int, left: int, right: int, start: int, end: int) -> int:
        if left >= start and right <= end:
            return self.tree[node]
        self._spread(node)
        mid = (left + right) // 2
        if end <= mid:
            return self._query(node * 2, left, mid, start, end)
        if start > mid:
            return self._query(node * 2 + 1, mid + 1, right, start, end)
        lr = self._query(node * 2, left, mid, start, end)
        rr = self._query(node * 2 + 1, mid + 1, right, start, end)
        return self._merge(lr, rr)

    def _update(self, node: int, left: int, right: int, start: int, end: int, val: int) -> None:
        if left >= start and right <= end:
            self._apply(node, val)
            return
        self._spread(node)
        mid = (left + right) // 2
        if start <= mid:
            self._update(node * 2, left, mid, start, end, val)
        if end > mid:
            self._update(node * 2 + 1, mid + 1, right, start, end, val)
        self._maintain(node)

    def _maintain(self, node: int) -> None:
        self.tree[node] = self._merge(self.tree[node * 2], self.tree[node * 2 + 1])

    def _spread(self, node: int) -> None:
        if self.mark[node] == 0:
            return
        self._apply(node * 2, self.mark[node])
        self._apply(node * 2 + 1, self.mark[node])
        self.mark[node] = 0

    def _apply(self, node: int, val: int) -> None:
        self.tree[node] += val
        self.mark[node] += val

    def _merge(self, v1: int, v2: int) -> int:
        return min(v1, v2)


class Solution:
    # time O(n * log(n)), space O(n + max(nums))
    def minCostSegmentTree(self, nums: list[int], k: int) -> int:
        # 线段树优化 DP: 将代价拆分, 用区间加减维护 distinct 的变化
        # O(n^2) DP 中: dp[i+1] = min(k + total - distinct + dp[j]) for j in [0, i]
        # 提取常数: = min(dp[j] - distinct(j, i)) + (i - j + 1) + k - 1
        # 线段树维护 dp[j] - distinct(j, i) 的最小值
        # 当处理第 i 个元素时:
        #   1. 该元素首次出现: 对 [last+1, i] 区间 -1 (这些 j 的 distinct +1)
        #   2. 该元素第二次出现: 对 [prev_to_last+1, last] 区间 +1
        #      (上次出现不再是"只出现一次", 撤销之前的 -1)
        # last[v]: 值 v 上一次出现的位置 (1-indexed)
        # prev_to_last[v]: 值 v 上上次出现的位置
        res, n = 0, len(nums)
        last = [0] * n
        prev_to_last = [0] * n
        st = SegmentTree(n)
        for i in range(1, n + 1):
            num = nums[i - 1]
            # 将 dp[i-1] (即 res) 写入线段树位置 i
            st.update(i, i, res)
            # nums[i] 出现, [last+1, i] 的 distinct 都 +1, 线段树值 -1
            st.update(last[num] + 1, i, -1)
            if last[num] > 0:
                # 上次出现位置 last 不再是"只出现一次"
                # 撤销之前对 [prev_to_last+1, last] 的 -1
                st.update(prev_to_last[num] + 1, last[num], 1)
            # 查询所有分割点的最小值
            res = k + st.query(1, i)
            prev_to_last[num] = last[num]
            last[num] = i
        # +n 是因为线段树维护的是 dp[j] - distinct, 还需要加上 total = n
        return res + n

    # time O(n^2), space O(n + max(nums))
    def minCostDP(self, nums: list[int], k: int) -> int:
        # trimmed(sub) 删除只出现一次的元素, 代价 = len(trimmed(sub)) + k
        # 即 代价 = (子数组长度 - 只出现一次的元素个数) + k
        #        = total - distinct + k
        # dp[i+1]: nums[0..i] 的最小总代价
        # 从 i 往前枚举最后一段 nums[j..i], 边扩展边维护 freq
        n, mx = len(nums), 0
        for x in nums:
            mx = max(mx, x)
        dp = [0] * (n + 1)
        for i in range(n):
            res, total, distinct = inf, 0, 0
            freq = [0] * (mx + 1)
            for j in range(i, -1, -1):
                if freq[nums[j]] == 0:
                    distinct += 1  # 新元素, 暂时算只出现一次
                if freq[nums[j]] == 1:
                    distinct -= 1  # 第二次出现, 不再是"只出现一次"
                total += 1
                freq[nums[j]] += 1
                # total - distinct = 出现次数 > 1 的元素总频次
                res = min(res, k + total - distinct + dp[j])
            dp[i + 1] = res
        return dp[n]

    # time O(n^2), space O(n + max(nums))
    def minCostDFSWithMemorization(self, nums: list[int], k: int) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): nums[0..i] 的最小总代价
        n, mx = len(nums), 0
        for x in nums:
            mx = max(mx, x)

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            res, total, distinct = inf, 0, 0
            freq = [0] * (mx + 1)
            for j in range(i, -1, -1):
                if freq[nums[j]] == 0:
                    distinct += 1
                if freq[nums[j]] == 1:
                    distinct -= 1
                total += 1
                freq[nums[j]] += 1
                res = min(res, k + total - distinct + dfs(j - 1))
            return res

        return dfs(n - 1)
