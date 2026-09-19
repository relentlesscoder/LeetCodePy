import pytest

from leetcodepy.problems.sliding_window.p2958_length_of_longest_subarray_with_at_most_k_frequency import (
    Solution,
)


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 2, 3, 1, 2, 3, 1, 2], 2, 6),  # LeetCode example 1: [1,2,3,1,2,3]
        ([1, 2, 1, 2, 1, 2, 1, 2], 1, 2),  # LeetCode example 2: [1,2]
        ([5, 5, 5, 5, 5, 5, 5], 4, 4),  # LeetCode example 3: [5,5,5,5]
        ([1], 1, 1),  # single element
        ([1, 2, 3, 4], 1, 4),  # all distinct, whole array
        ([2, 2, 2], 3, 3),  # k equals total count, whole array
        ([1, 1, 1, 2], 2, 3),  # [1,1,2] or [1,2] -> best is 3
    ],
)
def test_max_subarray_length(sol: Solution, nums: list[int], k: int, expected: int) -> None:
    assert sol.maxSubarrayLength(nums, k) == expected
