# 2707. Extra Characters in a String
# https://leetcode.com/problems/extra-characters-in-a-string/
# Difficulty: Medium


from functools import cache
from math import inf


class TrieNode:
    __slots__ = ("is_end", "nodes")

    def __init__(self):
        self.nodes = [None] * 26
        self.is_end = False


class Solution:
    # time O(n * L), space O(n + m * L)
    def minExtraCharDP(self, s: str, dictionary: list[str]) -> int:
        # Trie + DP: 类似 p0139, 单词反向插入 Trie
        # dp[i+1]: s[0..i] 的最少多余字符数
        # 两种选择: 1) s[i] 作为多余字符, dp[i+1] = dp[i] + 1
        #          2) s[j..i] 匹配字典单词, dp[i+1] = dp[j] (无多余字符)
        n = len(s)
        mx = 0
        root = TrieNode()
        for w in dictionary:
            self.insert(root, w)
            mx = max(mx, len(w))
        dp = [0] + [inf] * n
        for i in range(n):
            # 选择 1: 跳过 s[i], 多余字符 +1
            dp[i + 1] = min(dp[i + 1], 1 + dp[i])
            # 选择 2: 从 i 往前沿 Trie 匹配
            curr = root
            for j in range(i, max(i - mx, -1), -1):
                idx = ord(s[j]) - ord("a")
                if curr.nodes[idx] is None:
                    break
                curr = curr.nodes[idx]
                if curr.is_end:
                    # s[j..i] 匹配字典单词, 无多余字符
                    dp[i + 1] = min(dp[i + 1], dp[j])
        return dp[n]

    # time O(n * L), space O(n + m * L)
    def minExtraCharDFSWithMemorization(self, s: str, dictionary: list[str]) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的最少多余字符数
        n = len(s)
        mx = 0
        root = TrieNode()
        for w in dictionary:
            self.insert(root, w)
            mx = max(mx, len(w))

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0  # 空串, 0 个多余字符
            res = inf
            curr = root
            # 从 i 往前沿 Trie 匹配字典单词
            for j in range(i, max(i - mx, -1), -1):
                idx = ord(s[j]) - ord("a")
                if curr.nodes[idx] is None:
                    break
                curr = curr.nodes[idx]
                if curr.is_end:
                    res = min(res, dfs(j - 1))
            # 跳过 s[i] 作为多余字符
            return min(res, 1 + dfs(i - 1))

        return dfs(n - 1)

    def insert(self, root: TrieNode, s: str) -> None:
        # 将单词反向插入 Trie (因为从位置 i 往前匹配)
        curr = root
        for i in range(len(s) - 1, -1, -1):
            idx = ord(s[i]) - ord("a")
            if curr.nodes[idx] is None:
                curr.nodes[idx] = TrieNode()
            curr = curr.nodes[idx]
        curr.is_end = True
