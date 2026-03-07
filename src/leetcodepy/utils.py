"""Common LeetCode data structures."""

from __future__ import annotations

from collections import deque
from typing import Optional


# ── Linked List ──────────────────────────────────────────────────────────────

class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None) -> None:
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        nodes: list[int] = []
        cur: Optional[ListNode] = self
        seen: set[int] = set()
        while cur and id(cur) not in seen:
            nodes.append(cur.val)
            seen.add(id(cur))
            cur = cur.next
        return " -> ".join(map(str, nodes))


def list_to_linked(values: list[int]) -> Optional[ListNode]:
    """Build a linked list from a plain list."""
    if not values:
        return None
    head = ListNode(values[0])
    cur = head
    for v in values[1:]:
        cur.next = ListNode(v)
        cur = cur.next
    return head


def linked_to_list(head: Optional[ListNode]) -> list[int]:
    """Flatten a linked list into a plain list."""
    result: list[int] = []
    seen: set[int] = set()
    while head and id(head) not in seen:
        result.append(head.val)
        seen.add(id(head))
        head = head.next
    return result


# ── Binary Tree ──────────────────────────────────────────────────────────────

class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None,
    ) -> None:
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


def list_to_tree(values: list[int | None]) -> Optional[TreeNode]:
    """Build a binary tree from LeetCode's level-order list representation."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])  # type: ignore[arg-type]
    queue: deque[TreeNode] = deque([root])
    i = 1
    while queue and i < len(values):
        node = queue.popleft()
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])  # type: ignore[arg-type]
            queue.append(node.left)
        i += 1
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])  # type: ignore[arg-type]
            queue.append(node.right)
        i += 1
    return root


def tree_to_list(root: Optional[TreeNode]) -> list[int | None]:
    """Serialize a binary tree to LeetCode's level-order list representation."""
    if root is None:
        return []
    result: list[int | None] = []
    queue: deque[Optional[TreeNode]] = deque([root])
    while queue:
        node = queue.popleft()
        if node is None:
            result.append(None)
        else:
            result.append(node.val)
            queue.append(node.left)
            queue.append(node.right)
    # Strip trailing Nones
    while result and result[-1] is None:
        result.pop()
    return result
