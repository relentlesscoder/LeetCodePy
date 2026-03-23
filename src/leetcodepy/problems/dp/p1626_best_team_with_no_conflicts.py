# 1626. Best Team With No Conflicts
# https://leetcode.com/problems/best-team-with-no-conflicts/
# Difficulty: Medium


class Solution:
    # time O(n * log(m)), space O(m), m 为最大年龄
    def bestTeamScoreBinaryIndexedTree(self, scores: list[int], ages: list[int]) -> int:
        # 用树状数组优化 bestTeamScoreDPByAge 的内层查询
        # dp[age] 的前缀最大值查询 O(m) → 树状数组 O(log m)
        # bit.pre(age): 查询 age 范围 [1, age] 内的最大总分
        # bit.update(age, val): 更新 age 位置的最大总分
        m = max(ages)
        arr = sorted(zip(scores, ages))
        bit = BIT(m)
        for score, age in arr:
            # 当前球员的最大总分 = [1, age] 的前缀最大值 + score
            bit.update(age, bit.pre(age) + score)
        return bit.pre(m)

    # time O(n * m), space O(m), m 为最大年龄
    def bestTeamScoreDPByAge(self, scores: list[int], ages: list[int]) -> int:
        # 优化思路: 用 age 作为 dp 下标, 而非球员编号
        # dp[age]: 以该年龄结尾的最大总分
        # 按 score 升序遍历, 对当前球员的 age, 查 dp[0..age] 的最大值再加 score
        # 内层循环从 O(n) 变为 O(m), 当 m < n 时更快
        # 可进一步用树状数组优化内层为 O(log m)
        m = max(ages)
        arr = sorted(zip(scores, ages))
        dp = [0] * (m + 1)
        for score, age in arr:
            # 查找 age <= 当前 age 的最大总分
            mx = 0
            for j in range(age + 1):
                mx = max(mx, dp[j])
            dp[age] = mx + score
        return max(dp)

    # time O(n^2), space O(n)
    def bestTeamScoreDP(self, scores: list[int], ages: list[int]) -> int:
        # 无冲突条件: 年龄大的分数不能比年龄小的低
        # 按 (score, age) 升序排序后, score 已经非递减
        # 只需保证选出的子序列中 age 也是非递减的(即最长非递减子序列变体)
        # dp[i]: 以第 i 个球员结尾的最大总分
        # 转移: 在 j < i 中找 age[j] <= age[i] 的最大 dp[j], 加上 score[i]
        n = len(scores)
        arr = sorted(zip(scores, ages))
        dp = [0] * n
        for i, x in enumerate(arr):
            mx = 0
            for j in range(i):
                # score 已排序保证非递减, 只需检查 age 非递减
                if x[1] >= arr[j][1]:
                    mx = max(mx, dp[j])
            dp[i] = mx + x[0]
        return max(dp[i] for i in range(n))


class BIT:
    __slots__ = "tree"

    def __init__(self, n: int):
        self.tree = [0] * (n + 1)

    def update(self, index: int, val: int) -> None:
        while index < len(self.tree):
            self.tree[index] = max(self.tree[index], val)
            index += index & -index

    def pre(self, index: int) -> int:
        res = 0
        while index > 0:
            res = max(res, self.tree[index])
            index -= index & -index
        return res
