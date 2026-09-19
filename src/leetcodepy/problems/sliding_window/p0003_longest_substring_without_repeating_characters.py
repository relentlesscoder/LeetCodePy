# 3. Longest Substring Without Repeating Characters
# https://leetcode.com/problems/longest-substring-without-repeating-characters/
# Difficulty: Medium


class Solution:
    # 解法: 滑动窗口 + 记录字符上次出现位置 (左指针直接跳跃, 无需逐步收缩)
    # 时间复杂度 O(n): 只遍历字符串一次, 每轮都是 O(1) 操作
    # 空间复杂度 O(1): lastIndex 为固定大小 128 的数组, 与输入长度无关
    def lengthOfLongestSubstring(self, s: str) -> int:
        # res: 记录目前为止找到的最长无重复字符子串的长度
        # left: 窗口左边界 (窗口为闭区间 [left, right])
        res, left = 0, 0
        # lastIndex: 记录每个字符最近一次出现的下标, 下标为 ASCII 码 ord(c)
        # 初始值 -1 表示该字符还没出现过 (此时 lastIndex[ord(c)] + 1 == 0, 不影响 left)
        lastIndex = [-1] * 128
        for right, c in enumerate(s):
            # 1. 更新左边界: 如果 c 在窗口内出现过 (lastIndex[ord(c)] >= left),
            #    则 left 直接跳到上次出现位置的下一位, 一步跳过所有重复;
            #    取 max 保证 left 只会向右移动, 不会因为窗口外的旧记录而回退
            left = max(left, lastIndex[ord(c)] + 1)
            # 2. 更新答案: 此时窗口 [left, right] 内无重复字符,
            #    窗口长度为 right - left + 1
            res = max(res, right - left + 1)
            # 3. 记录 c 本次出现的位置, 供后续重复判断使用
            lastIndex[ord(c)] = right
        return res

    # 解法: 滑动窗口 (Sliding Window) + 定长数组计数
    # 时间复杂度 O(n): left 和 right 指针各自最多移动 n 次
    # 空间复杂度 O(1): counter 为固定大小 128 的数组, 与输入长度无关
    def lengthOfLongestSubstringSlidingWindow(self, s: str) -> int:
        # res: 记录目前为止找到的最长无重复字符子串的长度
        # left: 窗口左边界 (窗口为闭区间 [left, right])
        res, left = 0, 0
        # counter: 统计当前窗口内每个字符出现的次数
        # 使用固定大小 128 的数组覆盖全部 ASCII 字符 (相当于 Java 的 new int[128]),
        # 下标为字符的 ASCII 码 ord(c), 初始值全为 0, 比哈希表访问更快
        counter = [0] * 128

        # right 为窗口右边界, 每轮循环将字符 c = s[right] 加入窗口
        for right, c in enumerate(s):
            # 1. 扩大窗口: 把当前字符 c 计入窗口
            counter[ord(c)] += 1

            # 2. 收缩窗口: 如果 c 在窗口内出现超过一次, 说明产生了重复.
            #    注意: 只有刚加入的 c 可能重复, 其他字符的计数不会变化,
            #    所以只需检查 counter[ord(c)] > 1.
            #    不断把左边界的字符移出窗口, 直到 c 的计数恢复为 1,
            #    此时窗口内又是无重复字符的状态.
            while counter[ord(c)] > 1:
                counter[ord(s[left])] -= 1  # 左边界字符移出窗口, 计数减一
                left += 1  # 左边界右移一位

            # 3. 更新答案: 此时窗口 [left, right] 内无重复字符,
            #    窗口长度为 right - left + 1
            res = max(res, right - left + 1)

        return res
