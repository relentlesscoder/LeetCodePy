"""Shared pytest fixtures and helpers."""

import pytest

from leetcodepy.utils import (
    ListNode,
    TreeNode,
    linked_to_list,
    list_to_linked,
    list_to_tree,
    tree_to_list,
)


@pytest.fixture
def make_linked():
    """Return a factory: make_linked([1, 2, 3]) -> ListNode."""
    return list_to_linked


@pytest.fixture
def make_tree():
    """Return a factory: make_tree([1, 2, 3, None, None, 4]) -> TreeNode."""
    return list_to_tree


__all__ = [
    "ListNode",
    "TreeNode",
    "linked_to_list",
    "list_to_linked",
    "list_to_tree",
    "tree_to_list",
]
