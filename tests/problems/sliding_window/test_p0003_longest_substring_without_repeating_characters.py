import pytest

from leetcodepy.problems.sliding_window.p0003_longest_substring_without_repeating_characters import (
    Solution,
)


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("abcabcbb", 3),  # "abc"
        ("bbbbb", 1),  # "b"
        ("pwwkew", 3),  # "wke"
        ("", 0),  # empty string
        (" ", 1),  # single space
        ("au", 2),  # two distinct chars
        ("dvdf", 3),  # "vdf"
    ],
)
def test_length_of_longest_substring(sol: Solution, s: str, expected: int) -> None:
    assert sol.lengthOfLongestSubstring(s) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("abcabcbb", 3),  # "abc"
        ("bbbbb", 1),  # "b"
        ("pwwkew", 3),  # "wke"
        ("", 0),  # empty string
        (" ", 1),  # single space
        ("au", 2),  # two distinct chars
        ("dvdf", 3),  # "vdf"
    ],
)
def test_length_of_longest_substring_sliding_window(sol: Solution, s: str, expected: int) -> None:
    assert sol.lengthOfLongestSubstringSlidingWindow(s) == expected
