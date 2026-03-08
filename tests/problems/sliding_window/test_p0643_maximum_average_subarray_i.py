import pytest

from leetcodepy.problems.sliding_window.p0643_maximum_average_subarray_i import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums", "k", "expected"),
    [
        ([1, 12, -5, -6, 50, 3], 4, 12.75),  # window [12,-5,-6,50] -> 51/4
        ([5], 1, 5.0),                         # single element
        ([0, 4, 0, 3, 2], 1, 4.0),            # k=1, max single element
        ([3, 3, 3, 3], 4, 3.0),               # all same values
        ([-1, -2, -3, -4], 2, -1.5),          # all negatives
    ],
)
def test_find_max_average(sol: Solution, nums: list[int], k: int, expected: float) -> None:
    assert sol.findMaxAverage(nums, k) == pytest.approx(expected)
