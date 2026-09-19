# 2958. Length of Longest Subarray With at Most K Frequency
# https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/
# Difficulty: Medium


from collections import defaultdict


class Solution:
    # 解法: 滑动窗口 (Sliding Window) + 哈希表计数
    # 与 p0003 (阈值 1) / p3090 (阈值 2) 同一模板, 收缩阈值泛化为 k;
    # 元素是整数 (可达 10^9), 无法用定长数组, 改用 defaultdict 计数
    # 时间复杂度 O(n): left 和 right 指针各自最多移动 n 次, dict 操作均摊 O(1)
    # 空间复杂度 O(min(n, m)): m 为不同元素的个数, counter 最多存储窗口内的不同元素
    def maxSubarrayLength(self, nums: list[int], k: int) -> int:
        # res: 记录目前为止找到的最长合法子数组的长度
        # left: 窗口左边界 (窗口为闭区间 [left, right])
        res, left = 0, 0
        # counter: 统计当前窗口内每个数出现的次数
        # 使用 defaultdict(int), 访问不存在的键时默认值为 0
        counter = defaultdict(int)
        for right, num in enumerate(nums):
            # 1. 扩大窗口: 把当前数 num 计入窗口
            counter[num] += 1

            # 2. 收缩窗口: 如果 num 出现超过 k 次, 违反 "每个数最多出现 k 次" 的约束.
            #    只有刚加入的 num 可能超标, 所以只需检查 counter[num] > k.
            #    不断把左边界的数移出窗口, 直到 num 的计数降回 k,
            #    此时窗口重新满足约束 (循环不变量: 窗口内每个数最多出现 k 次)
            while counter[num] > k:
                counter[nums[left]] -= 1  # 左边界的数移出窗口, 计数减一
                left += 1  # 左边界右移一位

            # 3. 更新答案: 此时窗口 [left, right] 是以 right 结尾的最长合法窗口,
            #    窗口长度为 right - left + 1
            res = max(res, right - left + 1)
        return res
