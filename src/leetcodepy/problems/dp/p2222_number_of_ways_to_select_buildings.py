# 2222. Number of Ways to Select Buildings
# https://leetcode.com/problems/number-of-ways-to-select-buildings/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(n)
    def numberOfWays(self, s: str) -> int:
        # 枚举中间建筑. 选 3 个建筑使相邻不同类 (010 或 101).
        # 对每个位置 i 作为中间建筑:
        #   s[i]=='1': 左右各需一个 '0', 方案数 = left_0 * right_0
        #   s[i]=='0': 左右各需一个 '1', 方案数 = left_1 * right_1
        # 预处理左侧 0 的个数, 反向遍历时维护右侧 0 的个数.
        res, n, cnt = 0, len(s), 0
        left_zeros = [0] * n
        for i in range(n):
            left_zeros[i] = cnt  # i 左边的 '0' 个数
            cnt += 1 if s[i] == "0" else 0
        cnt = 0  # 右侧 '0' 个数
        for i in range(n - 1, -1, -1):
            if s[i] == "1":
                # 中间是 '1', 左右各需 '0'
                res += cnt * left_zeros[i]
            else:
                # 中间是 '0', 左右各需 '1'
                # right_1 = (n-i-1 - cnt), left_1 = (i - left_zeros[i])
                res += (n - i - 1 - cnt) * (i - left_zeros[i])
            cnt += 1 if s[i] == "0" else 0
        return res

    # time O(n), space O(1)
    def numberOfWaysDP(self, s: str) -> int:
        # 子序列选取 DP, 滚动数组. 从 s 中选 3 个字符使相邻不同类.
        # dp[j+1][k]: 已选 j+1 个字符, 最后选的是类型 k 的方案数.
        # 对每个位置 i (类型 x):
        #   k != x 时可以选 (交替), dp[j+1][k] += dp[j][x]
        #   k == x 时跳过 (相邻同类不合法)
        n = len(s)
        dp = [[1, 1]] + [[0, 0] for _ in range(3)]
        for i in range(n):
            x = ord(s[i]) - ord("0")
            for j in range(3):
                for k in range(2):
                    dp[j + 1][k] = dp[j + 1][k]
                    if k != x:  # 交替: 最后选的 k 与当前 x 不同, 可以选
                        dp[j + 1][k] += dp[j][x]
        return dp[3][0] + dp[3][1]

    # time O(n), space O(n)
    def numberOfWaysDPWithGrid(self, s: str) -> int:
        # 三维 DP, 显式保存每步状态, 便于理解.
        # dp[i+1][j+1][k]: 从 s[0..i] 中选了 j+1 个, 最后选的类型为 k 的方案数.
        n = len(s)
        dp = [[[1, 1]] + [[0, 0] for _ in range(3)] for _ in range(n + 1)]
        for i in range(n):
            x = ord(s[i]) - ord("0")
            for j in range(3):
                for k in range(2):
                    dp[i + 1][j + 1][k] = dp[i][j + 1][k]  # 不选 i
                    if k != x:  # 选 i (交替)
                        dp[i + 1][j + 1][k] += dp[i][j][x]
        return dp[n][3][0] + dp[n][3][1]

    # time O(n), space O(n)
    def numberOfWaysDFSWithMemorization(self, s: str) -> int:
        # 记忆化搜索 (自顶向下), 与三维 DP 等价.
        # dfs(i, j, k): 从 s[0..i] 中还需选 j+1 个, 右边已选的类型为 k 的方案数.
        # k == x 时当前位置不能选 (相邻同类), 只能跳过.
        # k != x 时可以跳过或选取 (选取后传入 x 作为新约束).
        n = len(s)

        @cache
        def dfs(i: int, j: int, k: int) -> int:
            if j == -1:
                return 1  # 已选够, 合法
            if i == -1:
                return 0  # 位置用完, 未选够
            x = ord(s[i]) - ord("0")
            if k == x:
                return dfs(i - 1, j, k)  # 同类, 只能跳过
            return dfs(i - 1, j, k) + dfs(i - 1, j - 1, x)  # 跳过 or 选取

        return dfs(n - 1, 2, 0) + dfs(n - 1, 2, 1)
