# 2407. Longest Increasing Subsequence II
# https://leetcode.com/problems/longest-increasing-subsequence-ii/
# Difficulty: Hard


class Solution:
    # time O(n * log(m)), space O(m)
    def lengthOfLISSegmentTree(self, nums: list[int], k: int) -> int:
        # 用线段树优化 DP: 以值域为下标, 线段树维护区间最大值
        # 对每个 nums[i], 查询值域 [nums[i]-k, nums[i]-1] 的最大 LIS 长度
        # 等价于 DP 解法中遍历所有 j 找满足差值条件的最大 dp[j]
        # 区间查询 O(log m) 替代暴力遍历 O(n)
        n = len(nums)
        m = max(nums)
        st = SegmentTree(m + 1)  # 值域 [0, m], 需要 m+1 个位置
        for i in range(n):
            # 查询满足严格递增且差值 <= k 的最大 LIS 长度
            lis = st.query(max(nums[i] - k, 0), max(nums[i] - 1, 0)) + 1
            # 更新值 nums[i] 位置的最大 LIS 长度
            st.update(nums[i], lis)
        return st.query_all()

    # time O(n^2), space O(n)
    def lengthOfLISDP(self, nums: list[int], k: int) -> int:
        # LIS 变体: 要求相邻元素差值 <= k 且严格递增
        # dp[i]: 以 nums[i] 结尾的最长递增子序列长度
        # 转移: 在 j < i 中找 0 < nums[i] - nums[j] <= k 的最大 dp[j], 加 1
        res = 0
        n = len(nums)
        dp = [0] * n
        for i in range(n):
            mx = 0
            for j in range(i):
                if nums[i] - nums[j] > 0 and nums[i] - nums[j] <= k:
                    mx = max(mx, dp[j])
            dp[i] = mx + 1
            res = max(res, dp[i])
        return res


# 线段树: 维护区间最大值, 支持单点更新 + 区间查询, 均为 O(log n)
# 用数组存储完全二叉树, 下标从 1 开始:
#   node 的左子 = node*2, 右子 = node*2+1
#   根节点 tree[1] 存整个区间的最大值
class SegmentTree:
    __slots__ = ("length", "tree")

    def __init__(self, n: int):
        self.length = n
        # 数组大小 = 2 * next_pow2(n), 即叶子数向上对齐到 2 的幂再乘 2
        self.tree = [0] * (2 << n.bit_length())

    def query_all(self) -> int:
        # 根节点存整个区间的最大值
        return self.tree[1]

    def query(self, start: int, end: int) -> int:
        # 查询 [start, end] 区间的最大值
        return self._query(1, 0, self.length - 1, start, end)

    def update(self, index: int, val: int) -> None:
        # 单点更新: 将 index 位置的值设为 val
        return self._update(1, 0, self.length - 1, index, val)

    def _update(self, node: int, left: int, right: int, index: int, val: int) -> None:
        if left == right:
            # 到达叶子节点, 直接更新
            self.tree[node] = val
            return
        mid = (left + right) // 2
        if index <= mid:
            # index 在左半区间
            self._update(node * 2, left, mid, index, val)
        else:
            # index 在右半区间
            self._update(node * 2 + 1, mid + 1, right, index, val)
        # 回溯时用子节点更新父节点
        self._maintain(node)

    def _query(self, node: int, left: int, right: int, start: int, end: int) -> int:
        if left >= start and right <= end:
            # 当前区间完全在查询范围内, 直接返回
            return self.tree[node]
        mid = (left + right) // 2
        if end <= mid:
            # 查询范围完全在左半区间
            return self._query(node * 2, left, mid, start, end)
        if start > mid:
            # 查询范围完全在右半区间
            return self._query(node * 2 + 1, mid + 1, right, start, end)
        # 查询范围跨越左右, 分别查询后合并
        left_res = self._query(node * 2, left, mid, start, end)
        right_res = self._query(node * 2 + 1, mid + 1, right, start, end)
        return self._merge(left_res, right_res)

    def _maintain(self, node: int) -> None:
        # 用左右子节点的值更新父节点
        self.tree[node] = self._merge(self.tree[node * 2], self.tree[node * 2 + 1])

    def _merge(self, v1: int, v2: int) -> int:
        # 合并操作: 取最大值 (改成 + 就变成区间求和线段树)
        return max(v1, v2)
