# 1964. Find the Longest Valid Obstacle Course at Each Position
# https://leetcode.com/problems/find-the-longest-valid-obstacle-course-at-each-position/
# Difficulty: Hard


from bisect import bisect_right


class Solution:
    # time O(n * log(n)), space O(n)
    def longestObstacleCourseAtEachPositionGreedy(self, obstacles: list[int]) -> list[int]:
        # 贪心 + 二分: 同 p0300, 但这里是非递减子序列, 所以 bisect_right
        n = len(obstacles)
        res = [0] * (n)
        arr = []
        for i in range(n):
            idx = bisect_right(arr, obstacles[i])
            res[i] = idx + 1
            if idx == len(arr):
                arr.append(obstacles[i])
            else:
                arr[idx] = obstacles[i]
        return res
