# Python 数据类型内存模型

## 一切皆对象

Python 中每个值都是一个**堆上的对象**，变量名只是对象的引用（指针）。变量是**便利贴**，可以随时重新贴到任何对象上（与 Java 变量是固定类型的盒子不同）。

```python
a = 42
b = a   # b 和 a 指向同一个对象

# 变量可以随时重新绑定到任意类型
i = 1
i = "hi"   # i 现在指向字符串，之前的 1 引用计数减一，可能被 GC
i = [1, 2]
```

`for` 循环每次迭代都**重新绑定**循环变量，循环结束后变量仍存在（保持最后一次迭代的值）：

```python
for i, c in enumerate(s1):
    pass  # 第一个循环结束后 i, c 保持最后的值

for i, c in enumerate(s2):
    pass  # i, c 被重新绑定，与第一个循环无关
```

## 不可变类型 (Immutable)

| 类型 | 存储方式 |
|------|---------|
| `int` | 小整数 (-5~256) 被缓存，大整数每次新建对象 |
| `float` | 堆上对象，64-bit double |
| `str` | 堆上对象，字符数组，intern 机制缓存短字符串 |
| `tuple` | 堆上对象，固定长度指针数组 |
| `bool` | `True`/`False` 是单例对象 |

```python
a = 256; b = 256; a is b   # True（缓存）
a = 257; b = 257; a is b   # False（新建）

s1 = "hello"; s2 = "hello"; s1 is s2  # True（intern）
```

## 可变类型 (Mutable)

**list** — 动态数组，存的是指针数组，扩容时 1.125x 增长：
```
list object
┌──────────┐
│ ob_size  │  → 当前长度
│ capacity │  → 分配容量
│ *items ──┼──→ [ *obj0, *obj1, *obj2, ... ]  （堆上指针数组）
└──────────┘
```

**dict** — 哈希表，Python 3.7+ 保证插入顺序：
```
dict object
┌──────────────┐
│ hash table   │  → 存 (hash, key_ptr, val_ptr)
│ indices[]    │  → 紧凑存储，负载因子 2/3 时扩容
└──────────────┘
```

**set** — 类似 dict，只有 key，无 value

## 赋值 vs 拷贝

```python
# 赋值：共享引用
a = [1, 2, 3]
b = a
b.append(4)
print(a)  # [1, 2, 3, 4]  ← a 也变了！

# 浅拷贝：顶层新建，元素仍共享
c = a.copy()   # 或 a[:]

# 深拷贝：完全独立
import copy
d = copy.deepcopy(a)
```

## 对 LeetCode DP 的影响

### `[[0] * n] * m` vs `[[0] * n for _ in range(m)]`

`[[0] * n] * m` 创建的是 **m 个指向同一个列表的引用**：

```
dp ──→ [ ref, ref, ref ]
          │     │     │
          └─────┴─────┴──→ [0, 0, 0]  ← 同一个对象！
```

```python
dp = [[0] * 3] * 3
dp[0][0] = 1
print(dp)  # [[1, 0, 0], [1, 0, 0], [1, 0, 0]]  ← 全变了！  ❌
```

`[[0] * n for _ in range(m)]` 每次循环**新建一个独立列表**：

```
dp ──→ [ ref0, ref1, ref2 ]
          │      │      │
          ↓      ↓      ↓
       [0,0,0] [0,0,0] [0,0,0]  ← 三个不同对象
```

```python
dp = [[0] * 3 for _ in range(3)]
dp[0][0] = 1
print(dp)  # [[1, 0, 0], [0, 0, 0], [0, 0, 0]]  ← 只改了一行  ✅
```

注意：`[0] * n` 本身是安全的，因为 `0` 是不可变 int，共享引用没问题。**只有嵌套可变对象（list）时才需要用列表推导式**。
