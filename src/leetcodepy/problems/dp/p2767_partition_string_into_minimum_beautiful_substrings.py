# 2767. Partition String Into Minimum Beautiful Substrings
# https://leetcode.com/problems/partition-string-into-minimum-beautiful-substrings/
# Difficulty: Medium


from functools import cache


class TrieNode:
    __slots__ = ("is_end", "nodes")

    def __init__(self):
        self.nodes = [None] * 2
        self.is_end = False


class Solution:
    # time O(n * L), space O(n + L)
    def minimumBeautifulSubstrings(self, s: str) -> int:
        # beautiful 子串 = 不含前导零的 5 的幂的二进制表示
        # 将所有 5 的幂反向(低位到高位)插入 Trie, 从 i 往前匹配
        # dp[i+1]: s[0..i] 的最少划分段数, 类似 p0139/p2707
        n, num = len(s), 1
        root = TrieNode()
        # 预处理: 将位数 <= n 的所有 5 的幂插入 Trie
        while num.bit_length() <= n:
            self.insert(root, num)
            num *= 5
        dp = [0] * (n + 1)
        for i in range(n):
            curr = root
            res = 1_000
            # 从 i 往前沿 Trie 匹配 5 的幂的二进制
            for j in range(i, -1, -1):
                idx = ord(s[j]) - ord("0")
                if curr.nodes[idx] is None:
                    break
                curr = curr.nodes[idx]
                if curr.is_end:
                    # s[j..i] 是 5 的幂的二进制表示
                    res = min(res, 1 + dp[j])
            dp[i + 1] = res
        return -1 if dp[n] > n else dp[n]

    # time O(n * L), space O(n + L)
    def minimumBeautifulSubstringsDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索版本, 逻辑同 DP
        # dfs(i): s[0..i] 的最少划分段数
        n, num = len(s), 1
        root = TrieNode()
        while num.bit_length() <= n:
            self.insert(root, num)
            num *= 5

        @cache
        def dfs(i: int) -> int:
            if i == -1:
                return 0
            curr = root
            res = 1_000
            for j in range(i, -1, -1):
                idx = ord(s[j]) - ord("0")
                if curr.nodes[idx] is None:
                    break
                curr = curr.nodes[idx]
                if curr.is_end:
                    res = min(res, 1 + dfs(j - 1))
            return res

        res = dfs(n - 1)
        return -1 if res > n else res

    def insert(self, root: TrieNode, num: int) -> None:
        # 将 num 的二进制从低位到高位插入 Trie
        # 与 dfs/dp 中从 i 往前(高位到低位)遍历方向匹配
        curr = root
        while num > 0:
            idx = num & 1  # 取最低位
            if curr.nodes[idx] is None:
                curr.nodes[idx] = TrieNode()
            curr = curr.nodes[idx]
            num >>= 1  # 右移, 处理下一位
        curr.is_end = True
