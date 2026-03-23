# 139. Word Break
# https://leetcode.com/problems/word-break/
# Difficulty: Medium


from functools import cache


class TrieNode:
    __slots__ = ("is_end", "nodes")

    def __init__(self):
        self.nodes = [None] * 26
        self.is_end = False


class Solution:
    # time O(n * L), space O(n + m * L)
    def wordBreakDP(self, s: str, wordDict: list[str]) -> bool:
        # Trie + DP: 将单词反向插入 Trie, 从每个位置 i 往前匹配
        # dp[i+1]: s[0..i] 能否被拆分 (偏移 1 方便边界处理)
        # 对每个 i, 从 i 往前走 Trie, 找到匹配的单词时检查 dp[j]
        n = len(s)
        root = TrieNode()
        mx = 0  # 最长单词长度, 用于限制内层循环范围
        for word in wordDict:
            mx = max(mx, len(word))
            self.insert(root, word)  # 反向插入 Trie
        dp = [True] + [False] * (n)
        for i in range(n):
            node = root
            # 从 i 往前最多走 mx 步, 沿 Trie 匹配
            for j in range(i, max(i - mx, -1), -1):
                idx = ord(s[j]) - ord("a")
                if node.nodes[idx] is None:
                    break  # Trie 中无此前缀, 提前剪枝
                node = node.nodes[idx]
                if node.is_end and dp[j]:
                    # s[j..i] 是字典中的单词, 且 s[0..j-1] 可拆分
                    dp[i + 1] = True
                    break
        return dp[n]

    # time O(n * L), space O(n + S)
    def wordBreakDFSWithMemorization(self, s: str, wordDict: list[str]) -> bool:
        # 记忆化搜索版本, 逻辑同上
        # dfs(i): s[0..i] 能否被拆分
        n = len(s)
        root = TrieNode()
        mx = 0
        for word in wordDict:
            mx = max(mx, len(word))
            self.insert(root, word)

        @cache
        def dfs(i: int) -> bool:
            if i == -1:
                return True  # 空串, 可拆分
            node = root
            for j in range(i, max(i - mx, -1), -1):
                idx = ord(s[j]) - ord("a")
                if node.nodes[idx] is None:
                    break
                node = node.nodes[idx]
                if node.is_end and dfs(j - 1):
                    return True
            return False

        return dfs(n - 1)

    def insert(self, root: TrieNode, s: str) -> None:
        # 将单词反向插入 Trie
        # 反向是因为 DP/DFS 从位置 i 往前扫描匹配
        node = root
        for i in range(len(s) - 1, -1, -1):
            idx = ord(s[i]) - ord("a")
            if node.nodes[idx] is None:
                node.nodes[idx] = TrieNode()
            node = node.nodes[idx]
        node.is_end = True
