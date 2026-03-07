import pytest

from leetcodepy.problems.arrays.p0001_two_sum import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


@pytest.mark.parametrize(
    ("nums", "target", "expected"),
    [
        ([2, 7, 11, 15], 9, [0, 1]),
        ([3, 2, 4], 6, [1, 2]),
        ([3, 3], 6, [0, 1]),
    ],
)
def test_two_sum(sol: Solution, nums: list[int], target: int, expected: list[int]) -> None:
    assert sol.twoSum(nums, target) == expected
