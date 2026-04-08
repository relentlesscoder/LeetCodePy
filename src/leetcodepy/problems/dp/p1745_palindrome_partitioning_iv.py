# 1745. Palindrome Partitioning IV
# https://leetcode.com/problems/palindrome-partitioning-iv/
# Difficulty: Hard


class Solution:
    # time O(n^2), space O(n)
    def checkPartitioningCentralExpansion(self, s: str) -> bool:
        # p0132 和 p2472
        # 中心扩展 + DP. 判断 s 能否分成恰好 3 段回文子串.
        # dp[i][j+1]: s[0..j] 能否被分成恰好 i 段回文子串.
        # dp[0][0] = True (空前缀, 0 段合法), 答案为 dp[3][n].
        # 对每个中心 j 向两边扩展, 发现回文 s[l..r] 时:
        #   若 dp[i][l] 为 True (前 l 个字符已分成 i 段), 则 dp[i+1][r+1] = True.
        # 省去 O(n^2) 的回文预处理表, 边扩展边更新.
        n = len(s)
        dp = [[True] + [False] * n] + [[False] * (n + 1) for _ in range(3)]
        for i in range(3):
            for j in range(n):
                # 奇数长度回文: 以 j 为中心
                l, r = j, j
                while l >= 0 and r < n and s[l] == s[r]:
                    # s[l..r] 是回文, 若前 l 个字符已分成 i 段, 则前 r+1 个可分成 i+1 段
                    dp[i + 1][r + 1] = dp[i + 1][r + 1] or dp[i][l]
                    l -= 1
                    r += 1
                # 偶数长度回文: 以 j, j+1 为中心
                l, r = j, j + 1
                while l >= 0 and r < n and s[l] == s[r]:
                    dp[i + 1][r + 1] = dp[i + 1][r + 1] or dp[i][l]
                    l -= 1
                    r += 1
        return dp[3][n]
