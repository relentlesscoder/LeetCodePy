# 2189. Number of Ways to Build House of Cards

https://leetcode.com/problems/number-of-ways-to-build-house-of-cards/
Difficulty: Medium (Premium)

## 题目描述

给定 `n` 张牌，搭纸牌屋。规则：
- 每一行由若干个三角形组成，每个三角形用 2 张牌，相邻三角之间放 1 张横牌
- 每一行的三角数必须**严格少于**下面一行
- 返回能搭出的不同纸牌屋数量

**关键公式：** 一行 `k` 个三角形需要 `3k - 1` 张牌

## 解题思路

### 记忆化搜索

`dfs(remaining, max_triangles)` = 剩余 `remaining` 张牌、当前行最多 `max_triangles - 1` 个三角的方案数

- 初始调用：`dfs(n, (n + 1) // 3 + 1)`，上界来自 `3k - 1 <= n → k <= (n + 1) / 3`
- 对每行尝试放 `k` 个三角（`1 <= k < max_triangles`），消耗 `3k - 1` 张牌
- 递归时约束下一行三角数 `< k`（严格递减）

```python
from functools import cache

class Solution:
    def houseOfCards(self, n: int) -> int:
        @cache
        def dfs(remaining: int, max_triangles: int) -> int:
            if remaining == 0:
                return 1  # 牌用完，合法
            res = 0
            for k in range(1, max_triangles):  # 当前行放 k 个三角，必须 < 上一行
                cost = 3 * k - 1
                if cost > remaining:
                    break   # k 越大 cost 越大，可以提前退出
                res += dfs(remaining - cost, k)
            return res

        return dfs(n, (n + 1) // 3 + 1)
```

### 翻译成 DP

`dp[r][m]` = 剩余 `r` 张牌、当前行最多 `m - 1` 个三角的方案数

转化关系：

| 记忆化搜索 | DP |
|---|---|
| `dfs(0, m) = 1` | `dp[0][m] = 1` |
| `dfs(r, m) += dfs(r - cost, k)` | `dp[r][m] += dp[r - cost][k]` |
| `dfs(n, max_t)` | `dp[n][max_t]` |

`dp[r][m]` 依赖 `dp[r - cost][k]`（`k < m`），所以 `m` 要从小到大计算：

```python
class Solution:
    def houseOfCards(self, n: int) -> int:
        max_t = (n + 1) // 3 + 1
        dp = [[0] * (max_t + 1) for _ in range(n + 1)]
        for m in range(max_t + 1):
            dp[0][m] = 1  # 0 张牌剩余 = 1 种方案

        for r in range(1, n + 1):
            for m in range(1, max_t + 1):
                for k in range(1, m):       # 当前行放 k 个三角，k < m
                    cost = 3 * k - 1
                    if cost > r:
                        break
                    dp[r][m] += dp[r - cost][k]

        return dp[n][max_t]
```

## 复杂度

- 时间：`O(n^2)`（每个状态 `(r, m)` 内层循环最多 `O(n/3)` 次）
- 空间：`O(n^2)`
