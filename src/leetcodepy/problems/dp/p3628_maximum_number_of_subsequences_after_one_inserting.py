# 3628. Maximum Number of Subsequences After One Inserting
# https://leetcode.com/problems/maximum-number-of-subsequences-after-one-inserting/
# Difficulty: Medium


class Solution:
    # time O(m), space O(1)
    def numOfSubsequences(self, s: str) -> int:
        # 前后缀分解
        cntL = cntLC = cntLCT = 0
        # 正向: 统计 cntL, cntLC, cntLCT
        for c in s:
            if c == "L":
                cntL += 1
            elif c == "C":
                cntLC += cntL
            elif c == "T":
                cntLCT += cntLC

        # 反向: 统计 cntCT 和 bestC
        cntT = 0
        cntCT = 0
        bestC = 0
        prefixL = cntL  # 当前位置左边(含)的 'L' 个数
        for i in range(len(s) - 1, -1, -1):
            if s[i] == "T":
                cntT += 1
            elif s[i] == "C":
                cntCT += cntT
            elif s[i] == "L":
                prefixL -= 1
            # 插入 'C' 在位置 i, 左边有 prefixL 个 'L', 右边有 cntT 个 'T'
            bestC = max(bestC, prefixL * cntT)

        extra = max(cntLC, cntCT, bestC)
        return cntLCT + extra

    # time O(m), space O(m)
    def numOfSubsequencesDP(self, s: str) -> int:
        t = "LCT"

        def insertToMiddle(s: str) -> int:
            # 插入 'C' 到位置 p，额外子序列 = s[0..p-1] 中 'L' 的个数 × s[p..m-1] 中 'T' 的个数
            # 枚举所有位置 p 取最大值
            res = 0
            m = len(s)
            # pre[i] = s[0..i-1] 中 'L' 的个数（前缀和）
            pre = [0] * (m + 1)
            for i, c in enumerate(s):
                pre[i + 1] = pre[i] + (1 if c == "L" else 0)
            # post = s[i..m-1] 中 'T' 的个数（从右往左累加）
            post = 0
            for i in range(m - 1, -1, -1):
                # 在位置 i+1 插入 'C'，左边有 pre[i+1] 个 'L'，右边有 post 个 'T'
                res = max(res, pre[i + 1] * post)
                post += 1 if s[i] == "T" else 0
            return res

        def numDistinct(s: str, t: str) -> int:
            # p0115 计算 s 中 t 子序列的个数
            m = len(s)
            n = len(t)
            dp = [1] + [0] * (n)
            for i in range(m):
                pre = dp[0]
                for j in range(n):
                    x = dp[j + 1]
                    if s[i] == t[j]:
                        dp[j + 1] += pre
                    pre = x
            return dp[n]

        # 三种插入选择取最优：
        # 1. 插入 'L' 到最前面 → 额外子序列 = s 中 "CT" 子序列的个数
        # 2. 插入 'T' 到最后面 → 额外子序列 = s 中 "LC" 子序列的个数
        # 3. 插入 'C' 到中间某位置 → 额外子序列 = 左边 'L' 个数 × 右边 'T' 个数
        extra = max(numDistinct(s, "LC"), numDistinct(s, "CT"), insertToMiddle(s))
        # 答案 = 原始 "LCT" 子序列数 + 最优插入带来的额外子序列数
        return numDistinct(s, t) + extra
