# 1567. Maximum Length of Subarray With Positive Product
# https://leetcode.com/problems/maximum-length-of-subarray-with-positive-product/
# Difficulty: Medium


from functools import cache


class Solution:
    # time O(n), space O(1)
    def getMaxLenDP(self, nums: list[int]) -> int:
        # 状态机 DP, 滚动变量. 求乘积为正的最长子数组.
        # 3 个状态: 正积 / 负积 / 零 (重置).
        #
        #            ┌──┐              ┌──┐
        #        *正 ▼  │          *正 ▼  │
        #          ┌─────┐  *负  ┌─────┐
        #          │ pos │◀─────▶│ neg │
        #          └─────┘       └─────┘
        #           ▲  │          ▲  │
        #       *正 │  │ *0   *负 │  │ *0
        #           │  ▼          │  ▼
        #          ┌──────────────────┐
        #      *0  │      zero        │
        #     ┌───▶│                  │◀──┐
        #     └────└──────────────────┘───┘
        #
        # pos*neg 互相翻转; 遇 0 全部重置; zero 遇正/负进入 pos/neg.
        #
        # p0: 以前一个元素结尾, 乘积为正的最长子数组长度
        # p1: 以前一个元素结尾, 乘积为负的最长子数组长度
        # 符号一致时 prev+1 天然处理 base case (0+1=1 = 单个元素);
        # 符号不一致时必须 prev > 0 (需要前面子数组来翻转符号).
        res, n, p0, p1 = 0, len(nums), 0, 0
        for i in range(n):
            c0, c1 = 0, 0
            if nums[i] == 0:
                c0 = 0  # 遇到 0, 全部重置
                c1 = 0
            elif nums[i] > 0:
                c0 = p0 + 1  # 正 * 正 = 正
                c1 = p1 + 1 if p1 > 0 else 0  # 负 * 正 = 负, 需要前面有负积
            else:
                c1 = p0 + 1  # 正 * 负 = 负 (或单个负数)
                c0 = p1 + 1 if p1 > 0 else 0  # 负 * 负 = 正, 需要前面有负积
            res = max(res, c0)
            p0 = c0
            p1 = c1
        return res

    # time O(n), space O(n)
    def getMaxLenDPWithGrid(self, nums: list[int]) -> int:
        # 数组 DP, 显式保存每步状态, 便于理解.
        # dp[i+1][0]: 以 nums[i] 结尾, 乘积为正的最长子数组长度
        # dp[i+1][1]: 以 nums[i] 结尾, 乘积为负的最长子数组长度
        res, n = 0, len(nums)
        dp = [[0, 0] for _ in range(n + 1)]
        for i in range(n):
            if nums[i] == 0:
                dp[i + 1][0] = 0
                dp[i + 1][1] = 0
            elif nums[i] > 0:
                dp[i + 1][0] = dp[i][0] + 1  # 正 * 正 = 正
                dp[i + 1][1] = dp[i][1] + 1 if dp[i][1] > 0 else 0  # 负 * 正 = 负
            else:
                dp[i + 1][1] = dp[i][0] + 1  # 正 * 负 = 负
                dp[i + 1][0] = dp[i][1] + 1 if dp[i][1] > 0 else 0  # 负 * 负 = 正
            res = max(res, dp[i + 1][0])
        return res

    def getMaxLenDFSWithMemorization(self, nums: list[int]) -> int:
        n = len(nums)

        @cache
        def dfs(i: int, j: int) -> int:
            # dfs(i, j): 以 nums[i] 结尾, 乘积符号为 j (0=正, 1=负) 的最长子数组长度
            # 关键: 当元素符号与目标一致时 (正数求正积 / 负数求负积),
            #   prev+1 在 prev=0 时得 1, 恰好表示"只选自己", 合法.
            #   当元素符号与目标不一致时 (负数求正积 / 正数求负积),
            #   必须有前面的子数组来翻转符号, 所以 prev 必须 > 0.
            if i == -1:
                return 0
            if nums[i] == 0:
                return 0  # 遇到 0, 子数组断开, 长度归零
            if j == 0:  # 需要正积
                if nums[i] > 0:  # 符号一致, 无需检查 prev
                    return dfs(i - 1, 0) + 1  # 正 * 正 = 正, prev=0 时为单个正数
                # 符号不一致, 需要前面有负积子数组来翻转
                prev = dfs(i - 1, 1)
                return prev + 1 if prev > 0 else 0
            # j == 1, 需要负积
            if nums[i] < 0:  # 符号一致, 无需检查 prev
                return dfs(i - 1, 0) + 1  # 正 * 负 = 负, prev=0 时为单个负数
            # 符号不一致, 需要前面有负积子数组来翻转
            prev = dfs(i - 1, 1)
            return prev + 1 if prev > 0 else 0

        # 最长正积子数组可能在任意位置结束, 需要对所有位置取 max
        return max(dfs(i, 0) for i in range(n))
