import pytest

from leetcodepy.problems.dp.p1774_closest_dessert_cost import Solution


@pytest.fixture
def sol() -> Solution:
    return Solution()


CASES = [
    ([1, 7], [3, 4], 10, 10),          # LeetCode example 1: exact match
    ([2, 3], [4, 5, 100], 18, 17),     # LeetCode example 2: closest below
    ([3, 10], [2, 5], 9, 8),           # closest is 8
    ([10], [1], 1, 10),                # base cost already exceeds target
    ([1], [1], 4, 3),                  # 1 base + 2 toppings = 3, closest to 4
]


@pytest.mark.parametrize(("baseCosts", "toppingCosts", "target", "expected"), CASES)
def test_closest_cost(
    sol: Solution,
    baseCosts: list[int],
    toppingCosts: list[int],
    target: int,
    expected: int,
) -> None:
    assert sol.closestCost(baseCosts, toppingCosts, target) == expected


@pytest.mark.parametrize(("baseCosts", "toppingCosts", "target", "expected"), CASES)
def test_closest_cost_dp_with_grid(
    sol: Solution,
    baseCosts: list[int],
    toppingCosts: list[int],
    target: int,
    expected: int,
) -> None:
    assert sol.closestCostDPWithGrid(baseCosts, toppingCosts, target) == expected


@pytest.mark.parametrize(("baseCosts", "toppingCosts", "target", "expected"), CASES)
def test_closest_cost_fs_with_memorization(
    sol: Solution,
    baseCosts: list[int],
    toppingCosts: list[int],
    target: int,
    expected: int,
) -> None:
    assert sol.closestCostFSWithMemorization(baseCosts, toppingCosts, target) == expected
