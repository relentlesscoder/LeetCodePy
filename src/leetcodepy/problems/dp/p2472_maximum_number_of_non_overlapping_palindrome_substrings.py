# 2472. Maximum Number of Non-overlapping Palindrome Substrings
# https://leetcode.cn/problems/maximum-number-of-non-overlapping-palindrome-substrings/
# Difficulty: Hard


class Solution:
    # time O(n * k), space O(n)
    def maxPalindromesDP(self, s: str, k: int) -> int:
        # 中心扩展 + DP: 类似 p0132
        # dp[i+1]: s[0..i] 中最多不重叠回文子串数 (长度 >= k)
        # 贪心: 找到长度 >= k 的回文后立即 break, 取最短的合法回文
        # 因为更短的回文留给后面更多空间, 不会更差
        n = len(s)
        if k == 1:
            return n  # 每个字符都是长度 1 的回文
        dp = [0] * (n + 1)
        for i in range(n):
            dp[i + 1] = max(dp[i + 1], dp[i])  # 不选任何以 i 结尾的回文
            # 奇数长度回文: 以 i 为中心扩展
            l, r = i, i
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 >= k:
                    dp[r + 1] = max(dp[r + 1], 1 + dp[l])
                    break  # 贪心取最短合法回文
                l -= 1
                r += 1
            # 偶数长度回文: 以 i, i+1 为中心扩展
            l, r = i, i + 1
            while l >= 0 and r < n and s[l] == s[r]:
                if r - l + 1 >= k:
                    dp[r + 1] = max(dp[r + 1], 1 + dp[l])
                    break
                l -= 1
                r += 1
        return dp[n]

    # time O(n^2), space O(n^2)
    def maxPalindromesDPWithPrecomputation(self, s: str, k: int) -> int:
        # 预处理回文表 + DP
        # 关键优化: 只需检查长度 k 和 k+1 的回文
        # 因为更长的回文一定包含长度 k 或 k+1 的回文子串, 贪心取短的更优
        n = len(s)
        if k == 1:
            return n
        # is_palin[i][j]: s[i..j] 是否回文
        is_palin = [[False] * n for _ in range(n)]
        for i in range(n - 1, -1, -1):
            for j in range(i, n, 1):
                is_palin[i][j] = s[i] == s[j] and (j - i <= 2 or is_palin[i + 1][j - 1])
        dp = [0] * (n + 1)
        for i in range(n):
            dp[i + 1] = dp[i]
            # 只检查长度 k (奇偶性同 k) 和 k+1 (奇偶性不同)
            for l in range(k, k + 2, 1):
                if i - l + 1 >= 0 and is_palin[i - l + 1][i]:
                    dp[i + 1] = max(dp[i + 1], 1 + dp[i - l + 1])
        return dp[n]
