# Python 语法速查

## 变量命名规则

### 语法规则 (强制, 违反报错)

1. 只能包含: 字母、数字、下划线 `_`; **不能以数字开头**
2. 区分大小写: `count` 和 `Count` 是两个变量
3. 不能用关键字: `class`, `def`, `for`, `if`, `lambda`, `return` 等
   (`import keyword; keyword.kwlist` 可查全表)

```python
my_var = 1      # ✅
_temp = 2       # ✅
var2 = 3        # ✅
2var = 4        # ❌ SyntaxError, 数字开头
my-var = 5      # ❌ 减号不合法
class = 6       # ❌ 关键字
```

### PEP 8 命名约定 (风格)

| 类型 | 风格 | 示例 |
|------|------|------|
| 变量 / 函数 / 方法 | `snake_case` 小写+下划线 | `max_len`, `find_max_average` |
| 类 | `PascalCase` 大驼峰 | `Solution`, `TreeNode` |
| 常量 | `UPPER_SNAKE_CASE` | `MAX_SIZE = 128` |
| 模块 / 文件名 | `snake_case` | `python_syntax.py` |
| 包 (目录) | 全小写, 最好无下划线 | `sliding_window` |

对比 Java: Java 的变量/方法用 `camelCase`, Python 用 `snake_case` ——
这是两个语言最大的风格差异。

### 下划线的特殊含义

```python
_internal      # 单前缀: 约定为内部使用 (类似 protected), import * 不会导入
__private      # 双前缀: 类中触发名称改写, 变成 _ClassName__private
__init__       # 双前后缀 (dunder): Python 保留的魔术方法, 不要自造
_              # 单独下划线: 表示"不使用的值", 如 for _ in range(n)
name_          # 后缀下划线: 避免与关键字冲突, 如 class_, type_
```

### 本 repo 的特例

题解方法名保留 LeetCode 原始的 `camelCase` 签名 (如 `lengthOfLongestSubstring`),
会触发 ruff N802 警告, 这是仓库约定接受的 (见 AGENTS.md);
测试函数名遵循 PEP 8 用 `snake_case` (如 `test_length_of_longest_substring`)。

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
s[i:j]          # 切片 [i, j), 即 substring
s[:3]           # "hel" 从头开始
s[2:]           # "llo" 到末尾
s[-2:]          # "lo" 最后2个
s[::-1]         # "olleh" 反转字符串 (返回新字符串, str 不可变)
```

## 排序

```python
# lambda: 匿名函数, lambda x: x[0] 等价于 def f(x): return x[0]
# key 参数接收一个函数, 对每个元素调用, 用返回值来比较大小

# 对 list 原地排序
nums.sort()
nums.sort(reverse=True)

# sorted(): 返回新 list, 不修改原数据, 可对任何可迭代对象排序
sorted(nums, key=lambda x: -x)

# 多级排序: key 返回 tuple, 逐级比较
arr.sort(key=lambda x: (x[0], -x[1]))    # 第一维升序, 第二维降序

# 两个 list 合并后按 l1 的值逆序排序
pairs = sorted(zip(l1, l2), key=lambda x: -x[0])

# 按另一个 list 的值排序
idx = sorted(range(len(a)), key=lambda i: b[i])
a = [a[i] for i in idx]

# 对 dict 按 value 排序
sorted(d.items(), key=lambda x: x[1])
```

**`sorted()` vs `list.sort()`:**

| | `sorted(x)` | `x.sort()` |
|---|---|---|
| 返回 | 新 list | `None` |
| 修改原数据 | 否 | 是 |
| 适用对象 | 任何可迭代 | 仅 list |

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

# zip: 将多个可迭代对象按位置配对, 返回 tuple
list(zip(a, b))                      # [(a0,b0), (a1,b1), ...] 元素是 tuple
[[x, y] for x, y in zip(a, b)]      # 元素是 list

# tuple 默认比较: 先比第一个元素, 相同再比第二个, 依此类推
# 所以 sorted(zip(a, b)) 先按 a 升序, a 相同按 b 升序
sorted(zip(scores, ages))            # [(1,5), (3,1), (3,2)]
```

**`tuple` vs `list`:**

| | `tuple` | `list` |
|---|---|---|
| 可变 | 否, 创建后不能改 | 是, 可增删改 |
| 语法 | `(1, 2)` | `[1, 2]` |
| 可作 dict key / set 元素 | 是 (可哈希) | 否 |
| 性能 | 稍快, 省内存 | 稍慢 |

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

## Set

```python
s = set()               # 空 set（注意 {} 是空 dict）
s = {1, 2, 3}           # 从值创建
s = set([1, 2, 2, 3])   # 从 list 创建（去重）→ {1, 2, 3}

s.add(4)                # 添加
s.remove(2)             # 删除（不存在会报错）
s.discard(2)            # 删除（不存在不报错）
3 in s                  # O(1) 判断是否存在
5 not in s              # O(1) 判断是否不存在

# |= 并集赋值
s |= {3, 4}             # s = {1, 2, 3, 4}
```

## Dict

```python
# Python 的 dict 就是 HashMap
d = {}                   # 空 dict
d = {"a": 1, "b": 2}    # 带初始值
d["c"] = 3               # 设置/更新值
d["a"]                   # 读取（不存在会 KeyError）
d.get("x", 0)            # 读取（不存在返回默认值 0）
"a" in d                 # O(1) 判断 key 是否存在（检查的是 key 不是 value）
del d["a"]               # 删除

# defaultdict: 访问不存在的 key 时自动用默认值初始化
from collections import defaultdict
d = defaultdict(int)     # 默认值 0
d[5] += 1                # 不需要先判断 key 是否存在
d = defaultdict(list)    # 默认值 []
d["key"].append(1)       # 自动创建空 list 再 append
```

## Deque (双端队列)

```python
from collections import deque
dq = deque()
```

```
        头部 (left/front)          尾部 (right/back)
        ┌───┬───┬───┬───┐
        │ 0 │ 1 │ 2 │ 3 │
        └───┴───┴───┴───┘
        dq[0]              dq[-1]
```

| 操作 | 方法 | 位置 | O |
|------|------|------|---|
| 尾部加入 | `dq.append(x)` | right | O(1) |
| 头部加入 | `dq.appendleft(x)` | left | O(1) |
| 尾部弹出 | `dq.pop()` | right | O(1) |
| 头部弹出 | `dq.popleft()` | left | O(1) |
| 看尾部 | `dq[-1]` | right | O(1) |
| 看头部 | `dq[0]` | left | O(1) |
| 长度 | `len(dq)` | | O(1) |
| 判空 | `if dq:` / `if not dq:` | | O(1) |

**Python vs Java Deque:**

| Python | Java | 位置 |
|--------|------|------|
| `append(x)` | `offerLast(x)` | 尾部 |
| `appendleft(x)` | `offerFirst(x)` | 头部 |
| `pop()` | `pollLast()` | 尾部 |
| `popleft()` | `pollFirst()` | 头部 |
| `dq[-1]` | `peekLast()` | 尾部 |
| `dq[0]` | `peekFirst()` | 头部 |

注意: Java 的 `push/pop` 操作**头部** (栈语义), 与 Python 的 `append/pop` 操作**尾部**方向相反。

## 遍历

```python
# range(stop)              → 0, 1, ..., stop-1
# range(start, stop)       → start, start+1, ..., stop-1
# range(start, stop, step) → start, start+step, ...
# stop 是开区间, 不包含

# enumerate: 同时拿到索引和值
for i, c in enumerate(arr):
    print(i, c)  # i 是索引, c 是值

# 倒序遍历
for c in reversed(s):        # 倒序遍历字符
for i in range(len(s) - 1, -1, -1):  # 倒序遍历带索引
for c in s[::-1]:            # 切片反转

# 带步长遍历 (从 i 开始, 每次加 k, 到 n 为止)
for j in range(i, n, k):    # j = i, i+k, i+2k, ...

# 自增: Python 没有 i++, 用 i += 1
i += 1

# C 风格 for 循环用 while 替代:
# for (int j = a, i = b; cond; j--, i++) → while
j, i = a, b
while j >= 0 and i < n:
    # ...
    j -= 1
    i += 1

# for (int i = 2; i * i <= n; i++) → while 或 isqrt
from math import isqrt
for i in range(2, isqrt(n) + 1):  # 用 isqrt 转成 range
    pass
```

## 字符操作

```python
# Python 没有 char 类型, 'a' 就是长度为 1 的 str
# 单引号和双引号完全等价: 'a' == "a"
# 函数参数传字符也是 str, 没有专门的 char 类型: def foo(c: str)

ord('a')                 # 97, 字符 → ASCII 码
chr(97)                  # 'a', ASCII 码 → 字符
ord('b') - ord('a')      # 1, 字符相减（不能直接 'b' - 'a'）

# 常见用法: 字符映射到 0-25
idx = ord(c) - ord('a')
# 位运算中标记字符
mask |= 1 << (ord(c) - ord('a'))
```

### 对比 Java: 字符/整数互转

Java 的 `char` 本质是 16 位整数, 可直接参与算术; Python 的字符是 `str`, 必须用
`ord()` / `chr()` 显式转换。

| Java | Python | 说明 |
|------|--------|------|
| `c - 'a'` | `ord(c) - ord('a')` | 小写字母映射到 0-25 |
| `c - '0'` | `ord(c) - ord('0')` 或 `int(c)` | 数字字符转数值 |
| `(char) (i + 'a')` | `chr(i + ord('a'))` | 整数转回字符 |
| `counter[c]++` | `counter[ord(c)] += 1` | 数组下标不能直接用字符 |

### 定长数组计数 (代替 HashMap)

```python
# Java: int[] counter = new int[128]
counter = [0] * 128          # 全 ASCII 字符
counter = [0] * 26           # 仅小写字母, 配合 ord(c) - ord('a')
lastIndex = [-1] * 128       # 记录字符上次出现位置, -1 表示未出现

counter[ord(c)] += 1                    # 全 ASCII, 直接用 ord(c) 做下标
counter[ord(c) - ord('a')] += 1         # 仅小写字母, 映射到 0-25
```

性能提示: 热循环中可先把 `ord('a')` 提出来, 避免每轮重复调用:

```python
base = ord('a')
for c in s:
    counter[ord(c) - base] += 1
```

选择建议:

| 方案 | 适用场景 |
|------|----------|
| `[0] * 26` / `[0] * 128` | 字符集已知且小 (小写字母/ASCII), 访问最快 |
| `defaultdict(int)` | 任意 Unicode / 字符集未知, 无需 ord(), 更 Pythonic |
| `Counter` | 需要 most_common() 等计数工具 |

注意: `[0] * n` 只适用于不可变元素; 2D 数组要用 `[[0] * n for _ in range(m)]`
(见上文 List 初始化)。

## 运算符优先级 (从高到低)

| 优先级 | 运算符 | 说明 |
|--------|--------|------|
| 最高 | `()` | 括号 |
| | `**` | 幂 (右结合) |
| | `+x` `-x` `~x` | 一元正、负、按位取反 |
| | `*` `/` `//` `%` | 乘、除、整除、取模 (**同级**) |
| | `+` `-` | 加、减 |
| | `<<` `>>` | 位移 |
| | `&` | 按位与 |
| | `^` | 按位异或 |
| | `\|` | 按位或 |
| | `==` `!=` `<` `>` `<=` `>=` `in` `not in` `is` | 比较 |
| | `not` | 逻辑非 |
| | `and` | 逻辑与 |
| 最低 | `or` | 逻辑或 |

同级运算符从左到右结合, 除了 `**` 是右结合。

## 位运算

```python
a & b        # AND
a | b        # OR
a ^ b        # XOR
~a           # NOT
a << 2       # 左移
a >> 1       # 右移

# 赋值简写
a |= b       # a = a | b
a &= b       # a = a & b
a ^= b       # a = a ^ b

# 常用技巧
n & 1             # 判断奇偶（最低位）
n & (n - 1)       # 去掉最低位的 1
1 << k            # 2^k
n >> k & 1        # 取第 k 位
n | (1 << k)      # 第 k 位设为 1
n & ~(1 << k)     # 第 k 位设为 0
i & -i            # 取最低位的 1（lowbit, 树状数组用）

# 二进制位数相关
x.bit_length()          # 二进制位数, 如 (10).bit_length() → 4 (1010)
x.bit_length() - 1      # 最高位 1 在第几位 (从 0 开始)
1 << (x.bit_length() - 1)  # 最高位 1 的值, 如 10 → 8 (1000)
```

## 二分查找 bisect

```python
from bisect import bisect_left, bisect_right

arr = [1, 3, 5, 5, 7, 9]

bisect_left(arr, 5)    # 2 → 第一个 >= 5 的位置 (< 5 的个数)
bisect_right(arr, 5)   # 4 → 第一个 > 5 的位置  (<= 5 的个数)
```

| 函数 | 返回 | 含义 |
|------|------|------|
| `bisect_left(arr, k)` | 第一个 `>= k` 的位置 | `< k` 的个数 |
| `bisect_right(arr, k)` | 第一个 `> k` 的位置 | `<= k` 的个数 |

元素不存在时两者返回相同值。

## List 操作

```python
arr.append(4)        # 末尾添加一个元素
arr.extend([5, 6])   # 末尾添加多个元素
arr += [7, 8]        # 同 extend

# 反转
arr.reverse()        # 原地反转, O(n), 无返回值
arr[::-1]            # 返回新数组, 不修改原数组

# 自定义对象的 list
nodes = [Node(i) for i in range(5)]
nodes[0].val         # 访问属性
```

## 类 (Class)

```python
class BIT:
    # __slots__: 用固定数组代替 __dict__ 存属性, 省内存但不能动态加属性
    # 创建大量小对象(如树节点)时有用, 平时可不写
    __slots__ = "tree"              # 单个属性
    # __slots__ = ("val", "left", "right")  # 多个属性用 tuple

    count = 0           # 类变量, 所有实例共享（类似 Java static）

    def __init__(self, n: int):   # 构造函数, self 是实例本身
        self.tree = [0] * n       # 实例变量, 每个实例独立
        BIT.count += 1

    def update(self, i: int, v: int) -> None:  # 方法, 第一个参数必须是 self
        self.tree[i] = v
```

### 关键注意点

```python
# 1. 调用自身方法必须用 self.
class Solution:
    def helper(self, x):
        return x + 1
    def solve(self, nums):
        self.helper(5)  # ✅
        helper(5)       # ❌ NameError

# 2. 没有访问控制, 靠命名约定（和 Java private 编译器强制禁止不同）
self.public = 1       # 公开, 随便访问
self._protected = 2   # 约定内部使用, 实际仍可访问, 看到 _ 就别从外部调用
self.__private = 3    # Python 把 __x 改写成 _类名__x, 还是能访问
# f.__private        # ❌ AttributeError
# f._Foo__private    # 3, 仍可访问

# 3. 不要把可变类型放在类变量上
class Bad:
    items = []          # ❌ 所有实例共享同一个 list！
class Good:
    def __init__(self):
        self.items = []  # ✅ 每个实例独立

# 4. 继承
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # 调用父类构造
        self.breed = breed
```

### 对比 Java

| | Python | Java |
|---|---|---|
| 构造函数 | `__init__(self)` | `ClassName()` |
| 调用自身方法 | `self.method()` 必须写 | `method()` 可省 this |
| 访问控制 | 无, 靠命名约定 | `private/protected/public` |
| 静态变量 | 类变量 | `static` |
| 类型声明 | 不需要（可选 type hint） | 必须 |
| 多继承 | 支持 | 不支持（用 interface） |
