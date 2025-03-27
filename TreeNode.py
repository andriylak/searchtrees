from collections import deque
import queue
from typing import Any, TypeVar, Union, Callable

T = TypeVar("T")

DEFAULT_COMPARATOR = lambda a, b: a - b

class _TreeNode:
    """
    A class representing a node in a tree structure.

    Each node contains a key, a value, and references to its left and right children.
    Additional metadata, such as `metaValue`, can also be stored for calculating auxiliary data in some node.

    Attributes:
        key: The key associated with the node. Defaults to None.
        value: The value stored in the node. Defaults to None.
        left: The left child of the node. Defaults to None.
        right: The right child of the node. Defaults to None.
        _metaValue: Optional metadata associated with the node. Defaults to None.
    """

    def __init__(
        self,
        key: Union[T, None] = None,
        value: Union[T, None] = None,
        left: Union["_TreeNode", None] = None,
        right: Union["_TreeNode", None] = None,
    ):
        """
        Initialize a tree node.

        Args:
            key: The key of the node.
            value: The value of the node.
            left: The left child of the node.
            right: The right child of the node.
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self._metaValue = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the tree node and its subtrees.

        The representation follows the format:
            key:value (left_subtree) ^ [right_subtree]

        Returns:
            str: A string representation of the tree node.
        """
        return f"{self.key}:{self.value} ({self.left}) ^ [{self.right}]"

    def __eq__(self: "_TreeNode", root: "_TreeNode") -> bool:
        """
        Returns True if two trees are identical (checks only keys).

        Args:
            root (_TreeNode): The root of the tree to compare with.

        Returns:
            bool: True if the trees are identical, False otherwise.

        Raises:
            TypeError: If `root` is not an instance of _TreeNode.
        """
        if not isinstance(root, _TreeNode):
            raise TypeError(f"Cannot compare _TreeNode with {type(root).__name__}")
        queue1 = deque([self])
        queue2 = deque([root])
        while queue1 and queue2:
            node1 = queue1.popleft()
            node2 = queue2.popleft()
            if node1.key != node2.key:
                return False
            if node1.left and node2.left:
                queue1.append(node1.left)
                queue2.append(node2.left)
            elif node1.left or node2.left:
                return False
            if node1.right and node2.right:
                queue1.append(node1.right)
                queue2.append(node2.right)
            elif node1.right or node2.right:
                return False
        return True

    def preorder(self) -> "_TreeNode":
        """
        Performs a pre-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            _TreeNode: Each node in the tree in pre-order traversal.
        """
        if not self:
            return
        stack = [self]
        while stack:
            node = stack.pop()
            yield node
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)

    def inorder(self) -> "_TreeNode":
        """
        Performs an in-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            _TreeNode: Each node in the tree in in-order traversal.
        """
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield node
                node = node.right

    def reverseorder(self) -> "_TreeNode":
        """
        Performs a reverse-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            _TreeNode: Each node in the tree in reverse-order traversal.
        """
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.right
            else:
                node = stack.pop()
                yield node
                node = node.left

    def postorder(self) -> "_TreeNode":
        """
        Performs a post-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            _TreeNode: Each node in the tree in post-order traversal.
        """
        stack = [self]
        visited = [False]
        while stack:
            node, vis = stack.pop(), visited.pop()
            if node:
                if vis:
                    yield node
                else:
                    stack.append(node)
                    visited.append(True)
                    stack.append(node.right)
                    visited.append(False)
                    stack.append(node.left)
                    visited.append(False)

    def levelorder(self) -> "_TreeNode":
        """
        Performs a level-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            _TreeNode: Each node in the tree in level-order traversal.
        """
        if not self:
            return
        queue = deque([self])
        while queue:
            node = queue.popleft()
            yield node
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    def kthLargestElement(self, k: int) -> Union["_TreeNode", None]:
        """
        Returns the k-th largest element in the tree.

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the largest element.

        Returns:
            _TreeNode or None: The k-th largest node, or None if k is bigger than the size of tree.

        Raises:
            TypeError: If `k` is not an integer.
        """
        if not isinstance(k, int):
            raise TypeError(f"The k must be an integer not {type(k).__name__}")
        for node in self.reverseorder():
            k -= 1
            if k == 0:
                return node
        return None

    def kthSmallestElement(self, k: int) -> Union["_TreeNode", None]:
        """
        Finds and returns the k-th smallest element in the binary search tree (BST).

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the smallest element.

        Returns:
            _TreeNode or None: The k-th smallest node, or None if k is bigger than the size of tree.

        Raises:
            TypeError: If `k` is not an integer.
        """
        if not isinstance(k, int):
            raise TypeError(f"The k must be an integer not {type(k).__name__}")
        for node in self.inorder():
            k -= 1
            if k == 0:
                return node
        return None

    def findmin(self) -> Union[T, None]:
        """
        Returns the smallest key in the tree.

        Returns:
            Key or None: The smallest key, or None if the tree is empty.
        """
        node = self.kthSmallestElement(1)
        return node.key if node else None

    def findmax(self) -> Union[T, None]:
        """
        Returns the largest key in the tree.

        Returns:
            Key or None: The largest key, or None if the tree is empty.
        """
        node = self.kthLargestElement(1)
        return node.key if node else None

    def size(self) -> int:
        """
        Returns the number of nodes in the tree.

        Returns:
            int: The number of nodes in the tree. An empty tree has a size of 0.
        """
        size = 0
        if self:
            for node in self.preorder():
                size += 1
        return size

