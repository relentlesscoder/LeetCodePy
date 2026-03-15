# Python 语法速查

## List 初始化

```python
# 全为 0
dp = [0] * n                          # [0, 0, 0, ..., 0]

# 全为某个值
dp = [float('inf')] * n               # [inf, inf, ...]

# 值等于索引
dp = list(range(n))                   # [0, 1, 2, ..., n-1]
dp = list(range(n + 1))               # [0, 1, 2, ..., n]

# 第一个为特定值，其余为另一个值
dp = [1] + [0] * n                    # [1, 0, 0, ..., 0]
dp = [0] + [float('inf')] * n        # [0, inf, inf, ..., inf]

# 2D array（正确写法）
dp = [[0] * n for _ in range(m)]      # ✅ 每行独立对象
dp = [[0] * n] * m                    # ❌ 所有行共享同一对象！

# 2D array，第一行值等于索引，其余行全为 0
dp = [list(range(n + 1))] + [[0] * (n + 1) for _ in range(m)]
# → [[0,1,2,...,n], [0,0,...,0], [0,0,...,0], ...]
```

## 字符串

```python
s = "hello"
len(s)          # 5，len() 是内置函数，调用 s.__len__()
s[i]            # 访问第 i 个字符
s[i:j]          # 切片 [i, j)
```

## 排序

```python
# 对 list 原地排序
nums.sort()
nums.sort(reverse=True)

# 按某个 key 排序（不修改原 list）
sorted(nums, key=lambda x: -x)

# 两个 list 合并后按 l1 的值逆序排序
pairs = sorted(zip(l1, l2), key=lambda x: -x[0])
```

## 数学

```python
from math import inf, isqrt

float('inf')    # 正无穷
inf             # 同上（from math import inf）
isqrt(n)        # 整数平方根，等价于 int(n ** 0.5)
n ** 0.5        # 浮点平方根
abs(x)          # 绝对值
```

## 常用内置

```python
min(a, b)       # 两数取小
max(a, b)       # 两数取大
sum(lst)        # 求和
any(lst)        # 任意为真
all(lst)        # 全部为真
```

## 数据类型范围

| 类型 | 范围 | 备注 |
|------|------|------|
| `int` | **无限制** | 任意精度大整数，不存在溢出 |
| `float` | ±1.8 × 10³⁰⁸ | 64 位双精度，约 15-17 位有效数字 |
| `bool` | `True`(1) / `False`(0) | 是 `int` 的子类 |
| `str` | 无长度限制 | 没有 `char` 类型，单字符就是长度为 1 的 `str` |

```python
# 特殊浮点值
float('inf')     # 正无穷
float('-inf')    # 负无穷
float('nan')     # 非数字

# 无穷大推荐用法
from math import inf    # ✅
from cmath import inf   # ❌ 得到 complex 类型的无穷大
```

对比 Java/C++：Python 的 `int` 不会溢出，不需要考虑 `Integer.MAX_VALUE` 的问题。

## 记忆化搜索 `@cache`

`functools.cache`（Python 3.9+）把函数的参数→返回值缓存到字典中，相同参数不重复计算。

```python
from functools import cache

@cache
def dfs(i: int, j: int) -> int:
    if i < 0 or j < 0:
        return 0
    return dfs(i - 1, j - 1) + 1
```

等价于手动维护一个 `memo` 字典：

```python
memo = {}
def dfs(i, j):
    if (i, j) not in memo:
        memo[(i, j)] = ...  # 计算并存入
    return memo[(i, j)]
```

**要求**：参数必须可哈希（`int`、`str`、`tuple` ✅，`list`、`dict` ❌）

**`@cache` vs `@lru_cache`**：
- `@cache` = `@lru_cache(maxsize=None)`，无大小限制
- `@lru_cache(maxsize=128)` 默认最多缓存 128 个结果

**记忆化搜索 vs DP 数组**：

| | `@cache`（自顶向下） | DP 数组（自底向上） |
|---|---|---|
| 存储 | 字典 `dict` | 数组 `list` |
| 速度 | 稍慢（函数调用+哈希开销） | 稍快 |
| 空间优化 | 不容易 | 可压缩为一维/滚动数组 |
| 写法 | 更直观，接近递推公式 | 需想清楚遍历顺序 |

做题思路：先写 DFS + `@cache` → 翻译成 DP 数组 → 优化空间。
