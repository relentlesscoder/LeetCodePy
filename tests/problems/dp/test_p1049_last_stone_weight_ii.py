import pytest

from leetcodepy.problems.dp.p1049_last_stone_weight_ii import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


CASES = [
    ([2, 7, 4, 1, 8, 1], 1),   # LeetCode example 1
    ([31, 26, 33, 21, 40], 5),  # LeetCode example 2
    ([1], 1),                   # single stone
    ([1, 1], 0),                # two equal stones cancel out
    ([1, 2], 1),                # two stones, difference = 1
]


@pytest.mark.parametrize(("stones", "expected"), CASES)
def test_last_stone_weight_ii_dp(sol: Solution, stones: list[int], expected: int) -> None:
    assert sol.lastStoneWeightIIDP(stones) == expected


@pytest.mark.parametrize(("stones", "expected"), CASES)
def test_last_stone_weight_ii_dp_with_grid(sol: Solution, stones: list[int], expected: int) -> None:
    assert sol.lastStoneWeightIIDPWithGrid(stones) == expected


@pytest.mark.parametrize(("stones", "expected"), CASES)
def test_last_stone_weight_ii_dfs_with_memorization(sol: Solution, stones: list[int], expected: int) -> None:
    assert sol.lastStoneWeightIIDFSWithMemorization(stones) == expected
