# DP Notes

## Python List Initialization

**多一层括号 = 多一个维度**
```python
[0] + [1] * 3        # → [0, 1, 1, 1]        1D
[[0] + [1] * 3]      # → [[0, 1, 1, 1]]       2D (套了一层)
```

**`*` 的陷阱**
```python
[[0] * 3] * 2        # ❌ 两行是同一个对象
[[0] * 3 for _ in range(2)]  # ✅ 独立的两行
```

**初始化套路总结**

| 目标 | 写法 |
|------|------|
| 1D，全0 | `[0] * n` |
| 1D，自定义首元素 | `[0] + [1] * k` |
| 2D，全0 | `[[0] * cols for _ in range(rows)]` |
| 2D，首行特殊 | `[[0] + [1] * k] + [[0] * (k+1) for _ in range(n)]` |
| 3D | `[[[0] * depth for _ in range(cols)] for _ in range(rows)]` |
