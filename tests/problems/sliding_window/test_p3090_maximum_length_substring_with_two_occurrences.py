import pytest

from leetcodepy.problems.sliding_window.p3090_maximum_length_substring_with_two_occurrences import (
    Solution,
)


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("bcbbbcba", 4),  # LeetCode example 1: "bcbb"
        ("aaaa", 2),  # LeetCode example 2: "aa"
        ("a", 1),  # single char
        ("ab", 2),  # two distinct chars
        ("abcdef", 6),  # all unique, whole string
        ("aabbcc", 6),  # each char exactly twice, whole string
        ("aaabbb", 4),  # "aabb" (max two of each)
    ],
)
def test_maximum_length_substring(sol: Solution, s: str, expected: int) -> None:
    assert sol.maximumLengthSubstring(s) == expected
