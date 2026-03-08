import pytest

from leetcodepy.problems.dp.p0494_target_sum import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


CASES = [
    ([1, 1, 1, 1, 1], 3, 5),   # 5 ways to reach target 3
    ([1], 1, 1),                # only +1 works
    ([1], -1, 1),               # only -1 works
    ([1], 2, 0),                # impossible
    ([0, 0, 0], 0, 8),          # 2^3 = 8 ways with all zeros
]


@pytest.mark.parametrize(("nums", "target", "expected"), CASES)
def test_find_target_sum_ways(sol: Solution, nums: list[int], target: int, expected: int) -> None:
    assert sol.findTargetSumWaysDP(nums, target) == expected


@pytest.mark.parametrize(("nums", "target", "expected"), CASES)
def test_find_target_sum_ways_dp_with_grid(sol: Solution, nums: list[int], target: int, expected: int) -> None:
    assert sol.findTargetSumWaysDPWithGrid(nums, target) == expected


@pytest.mark.parametrize(("nums", "target", "expected"), CASES)
def test_find_target_sum_ways_dfs_with_memorization(sol: Solution, nums: list[int], target: int, expected: int) -> None:
    assert sol.findTargetSumWaysDFSWithMemorization(nums, target) == expected
