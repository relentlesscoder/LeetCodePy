# 376. Wiggle Subsequence
# https://leetcode.com/problems/wiggle-subsequence/
# Difficulty: Medium


class Solution:
    # time O(n), space O(1)
    def wiggleMaxLengthGreedy(self, nums: list[int]) -> int:
        # 贪心. 求最长摆动子序列 (交替上升下降).
        # up:   以上升结尾的最长摆动子序列长度
        # down: 以下降结尾的最长摆动子序列长度
        # 贪心性质: nums[i] > nums[i-1] 时, down 子序列的末尾总能调整到
        #   <= nums[i-1] < nums[i], 保证接上后合法. 因为如果原末尾 v >= nums[i],
        #   可以把 v 替换成 nums[i-1] (仍满足下降, 且 < nums[i] 可以接上升).
        #   反向同理. 所以只需比较相邻元素, 无需回溯.
        up, down, n = 1, 1, len(nums)
        for i in range(1, n, 1):
            if nums[i] > nums[i - 1]:
                up = down + 1  # 上升: 接在下降后面
            elif nums[i] < nums[i - 1]:
                down = up + 1  # 下降: 接在上升后面
            # 相等: 不构成摆动, 跳过
        return max(up, down)

    # time O(n^2), space O(n)
    def wiggleMaxLengthDPWithGrid(self, nums: list[int]) -> int:
        # 子序列选取 DP. 枚举所有前一个元素 j, 取最优.
        # dp[i][0]: 以 nums[i] 结尾, 最后一步上升的最长摆动子序列长度
        # dp[i][1]: 以 nums[i] 结尾, 最后一步下降的最长摆动子序列长度
        res, n = 0, len(nums)
        dp = [[1, 1] for _ in range(n)]
        for i in range(n):
            for j in range(i):
                if nums[i] == nums[j]:
                    continue
                elif nums[i] > nums[j]:
                    # nums[j] → nums[i] 上升, 接在以 j 结尾的下降后面
                    dp[i][0] = max(dp[i][0], dp[j][1] + 1)
                else:
                    # nums[j] → nums[i] 下降, 接在以 j 结尾的上升后面
                    dp[i][1] = max(dp[i][1], dp[j][0] + 1)
            res = max(res, dp[i][0], dp[i][1])
        return res
