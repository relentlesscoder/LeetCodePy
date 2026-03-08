# 1456. Maximum Number of Vowels in a Substring of Given Length
# https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/
# Difficulty: Medium


class Solution:

    # time O(n), space O(1)
    def maxVowels(self, s: str, k: int) -> int:
        res = 0
        vowel = 0
        for i, c in enumerate(s):
            if c in "aeiou":
                vowel += 1

            left = i - k + 1
            if left < 0:
                continue
            
            res = max(res, vowel)
            if res == k:
                break

            if s[left] in "aeiou":
                vowel -= 1
        return res
