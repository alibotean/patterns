"""
Iterator Pattern

Intent: Provide a way to access the elements of an aggregate object sequentially
without exposing its underlying representation.

Python approach: implement __iter__ and __next__ to make any object work with
Python's for-loop, comprehensions, and the full iteration protocol.
The internal data structure stays private.

Example: a binary search tree with pluggable traversal strategies.
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import Generator, Iterator


# ── Node ──────────────────────────────────────────────────────────────────────

@dataclass
class _Node:
    value: int
    left:  "_Node | None" = field(default=None, repr=False)
    right: "_Node | None" = field(default=None, repr=False)


# ── Aggregate ─────────────────────────────────────────────────────────────────

class BinarySearchTree:
    """
    A BST whose internal node structure is never exposed to callers.
    Three iterators give different traversal orders using generators.
    """

    def __init__(self) -> None:
        self._root: _Node | None = None

    def insert(self, value: int) -> None:
        """Standard BST insertion."""
        if self._root is None:
            self._root = _Node(value)
            return
        node = self._root
        while True:
            if value < node.value:
                if node.left is None:  node.left  = _Node(value); return
                node = node.left
            else:
                if node.right is None: node.right = _Node(value); return
                node = node.right

    # ── Iterator factories ────────────────────────────────────────────────────

    def inorder(self) -> Iterator[int]:
        """Left → Root → Right  (yields sorted order for a BST)."""
        def _inorder(node: _Node | None) -> Generator[int, None, None]:
            if node:
                yield from _inorder(node.left)
                yield node.value
                yield from _inorder(node.right)
        return _inorder(self._root)

    def preorder(self) -> Iterator[int]:
        """Root → Left → Right  (useful for copying the tree structure)."""
        def _preorder(node: _Node | None) -> Generator[int, None, None]:
            if node:
                yield node.value
                yield from _preorder(node.left)
                yield from _preorder(node.right)
        return _preorder(self._root)

    def level_order(self) -> Iterator[int]:
        """Breadth-first (level by level) — iterative, no recursion."""
        if not self._root:
            return iter([])

        def _bfs() -> Generator[int, None, None]:
            queue = deque([self._root])
            while queue:
                node = queue.popleft()
                yield node.value          # type: ignore[union-attr]
                if node.left:  queue.append(node.left)   # type: ignore[union-attr]
                if node.right: queue.append(node.right)  # type: ignore[union-attr]

        return _bfs()

    def __iter__(self) -> Iterator[int]:
        """Default iteration = in-order (sorted), enabling: for x in tree."""
        return self.inorder()

    def __contains__(self, value: int) -> bool:
        """Enables: 42 in tree  — implemented with the iterator, not direct access."""
        return any(v == value for v in self)


# ── Demo ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    bst = BinarySearchTree()
    for val in [5, 3, 7, 1, 4, 6, 8]:
        bst.insert(val)

    print("In-order    (sorted):", list(bst.inorder()))
    print("Pre-order   (structural):", list(bst.preorder()))
    print("Level-order (BFS):", list(bst.level_order()))

    print("\nDefault for-loop (in-order):")
    for value in bst:
        print(f"  {value}")

    print("\nMembership test (uses __iter__):")
    print(f"  4 in bst → {4 in bst}")
    print(f"  9 in bst → {9 in bst}")
