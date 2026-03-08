import pytest

from leetcodepy.problems.sliding_window.p1456_maximum_number_of_vowels_in_a_substring_of_given_length import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("s", "k", "expected"),
    [
        ("abciiidef", 3, 3),   # "iii" has 3 vowels
        ("aeiou", 2, 2),       # any window of 2 has 2 vowels
        ("leetcode", 3, 2),    # "lee" or "eet" has 2 vowels
        ("rhythms", 4, 0),     # no vowels at all
        ("tryhard", 4, 1),     # best window has 1 vowel
    ],
)
def test_max_vowels(sol: Solution, s: str, k: int, expected: int) -> None:
    assert sol.maxVowels(s, k) == expected
