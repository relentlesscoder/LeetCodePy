# 960. Delete Columns to Make Sorted III
# https://leetcode.com/problems/delete-columns-to-make-sorted-iii/
# Difficulty: Hard


class Solution:
    # time O(n^2 * m), space O(n), n 为列数, m 为行数
    def minDeletionSizeDP(self, strs: list[str]) -> int:
        # 保留最多的列使每行剩余字符非递减 → 最少删除 = n - 最多保留
        # 转化为多维 LIS: 对列下标求最长子序列, 要求保留的列在每行都非递减
        # dp[i]: 以第 i 列结尾的最长可保留列子序列长度
        # ge(i, j): 第 i 列在所有行都 >= 第 j 列 (多维非递减条件)
        n = len(strs[0])
        res = n
        dp = [0] * n

        def ge(i: int, j: int) -> bool:
            m = len(strs)
            return all(strs[k][i] >= strs[k][j] for k in range(m))

        for i in range(n):
            mx = 0
            for j in range(i):
                if ge(i, j):
                    mx = max(mx, dp[j])
            dp[i] = mx + 1
            res = min(res, n - dp[i])
        return res
