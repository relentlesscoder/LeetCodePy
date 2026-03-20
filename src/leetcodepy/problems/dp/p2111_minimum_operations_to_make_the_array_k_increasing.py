# 2111. Minimum Operations to Make the Array K-Increasing
# https://leetcode.com/problems/minimum-operations-to-make-the-array-k-increasing/
# Difficulty: Hard


from bisect import bisect_right


class Solution:
    # time O(n * log(n)), space O(n)
    def kIncreasing(self, arr: list[int], k: int) -> int:
        # k-increasing 要求: 对所有 i >= k, arr[i] >= arr[i - k]
        # 即下标模 k 同余的元素各自构成非递减序列
        # 分成 k 组独立子序列, 每组求最长非递减子序列(LIS 变体)
        # 每组最少操作次数 = 子序列长度 - 最长非递减子序列长度
        n = len(arr)
        res = 0
        for i in range(k):
            # 对第 i 组 (下标 i, i+k, i+2k, ...) 求最长非递减子序列
            cnt = 0  # 该组元素个数
            nums = []  # 贪心维护的单调数组(类似 patience sorting)
            for j in range(i, n, k):
                cnt += 1
                # bisect_right: 因为允许相等(非递减), 用右侧插入点
                idx = bisect_right(nums, arr[j])
                if idx == len(nums):
                    # arr[j] >= nums 中所有元素, 直接追加, 子序列长度+1
                    nums.append(arr[j])
                else:
                    # 替换 nums[idx] 使数组尽可能小, 为后续元素留更多空间
                    nums[idx] = arr[j]
            # 该组需要修改的元素数 = 组长度 - 最长非递减子序列长度
            res += cnt - len(nums)
        return res
