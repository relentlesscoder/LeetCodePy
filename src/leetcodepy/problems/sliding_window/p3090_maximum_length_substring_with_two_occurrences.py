# 3090. Maximum Length Substring With Two Occurrences
# https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/
# Difficulty: Easy


class Solution:
    # 解法: 滑动窗口 (Sliding Window) + 定长数组计数
    # 与 p0003 的 counter 解法同一模板, 只是收缩阈值从 "出现 1 次" 放宽到 "出现 2 次"
    # 时间复杂度 O(n): left 和 right 指针各自最多移动 n 次
    # 空间复杂度 O(1): counter 为固定大小 26 的数组, 与输入长度无关
    def maximumLengthSubstring(self, s: str) -> int:
        # res: 记录目前为止找到的最长合法子串的长度
        # left: 窗口左边界 (窗口为闭区间 [left, right])
        res, left = 0, 0
        # counter: 统计当前窗口内每个字符出现的次数
        # 题目保证仅小写字母, 用大小 26 的数组, 下标为 ord(c) - ord("a") 映射到 0-25
        counter = [0] * 26
        for right, c in enumerate(s):
            # 1. 扩大窗口: 把当前字符 c 计入窗口
            idx = ord(c) - ord("a")
            counter[idx] += 1

            # 2. 收缩窗口: 如果 c 出现了 3 次, 违反 "每个字符最多出现 2 次" 的约束.
            #    只有刚加入的 c 可能超标, 所以只需检查 counter[idx] > 2.
            #    不断把左边界的字符移出窗口, 直到 c 的计数降回 2,
            #    此时窗口重新满足约束 (循环不变量: 窗口内每个字符最多出现 2 次)
            while counter[idx] > 2:
                counter[ord(s[left]) - ord("a")] -= 1  # 左边界字符移出窗口, 计数减一
                left += 1  # 左边界右移一位

            # 3. 更新答案: 此时窗口 [left, right] 是以 right 结尾的最长合法窗口,
            #    窗口长度为 right - left + 1
            res = max(res, right - left + 1)
        return res
