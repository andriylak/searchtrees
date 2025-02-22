from collections import deque
import queue
from typing import Any, TypeVar, Union, Callable


T = TypeVar("T")


class TreeNode:
    def __init__(
        self,
        key: T | None = None,
        value: T | None = None,
        left: T | None = None,
        right: T | None = None,
        calculate_func: Callable[[T], int]| None = None,
    ):
        """
        Initialize a tree node.
        :param key: The key of the node.
        :param value: The value of the node.
        :param left: The left child of the node.
        :param right: The right child of the node.
        :param calculate_func: Function, which explain how to calculate the weight of the each node.
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        self.calculate_func = calculate_func if calculate_func else lambda a: a
        self.metaValue = None

    def calculate_meta_value(self, func: Callable[[T], T]) -> T:
        stack = [self]
        visited = [False]
        while stack:
            node, vis = stack.pop(), visited.pop()
            if node:
                if vis:
                    node.metaValue = func(
                        left_subtree=node.left.metaValue if node.left else None,
                        right_subtree=node.right.metaValue if node.right else None,
                        node_value=node.value,
                    )
                    if node.left:
                        node.left.metaValue = None
                    if node.right:
                        node.right.metaValue = None
                else:
                    stack.append(node)
                    visited.append(True)
                    stack.append(node.right)
                    visited.append(False)
                    stack.append(node.left)
                    visited.append(False)
        result = self.metaValue
        self.metaValue = None
        return result

    def getMetaValue(self, target_key: T, func: Callable[[T], T]) -> T:
        """
        Returns the auxiliary data of the key if exists or it returns None if key does not exist
        :param target_key: The key of the node for which meta value will be calculated.
        :param function:  Function, which explain how to calculate mata value in the each node
        """
        if self.empty():
            return None
        current = self
        while current:
            if self.comparator(current.key, target_key) == 0:
                return current.calculate_meta_value(func)
            elif self.comparator(current.key, target_key) > 0:
                current = current.left
            else:
                current = current.right
        return None

    def comparator(self, value1, value2):
        return self.calculate_func(value1) - self.calculate_func(value2)

    def __repr__(self) -> str:
        return f"{self.key} ({self.left}) ^ [{self.right}]"

    def __eq__(self, root: "TreeNode") -> bool:
        """
        checks whether two trees are identical
        """
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

    def preorder(self) -> list[T]:
        """
        returns the list of keys in pre-order traversal
        """
        if self.empty():
            return []
        result = []
        stack = [self]
        while stack:
            node = stack.pop()
            result.append(node.key)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    def inorder(self) -> list[T]:
        """
        returns the list of elements in in-order traversal
        """
        if self.empty():
            return []
        result = []
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                result.append(node.key)
                node = node.right
        return result

    def postorder(self) -> list[T]:
        """
        returns the list of keys in post-order traversal
        """
        if self.empty():
            return []
        result = []
        stack = [self]
        visited = [False]
        while stack:
            node, vis = stack.pop(), visited.pop()
            if node:
                if vis:
                    result.append(node.key)
                else:
                    stack.append(node)
                    visited.append(True)
                    stack.append(node.right)
                    visited.append(False)
                    stack.append(node.left)
                    visited.append(False)
        return result

    def levelorder(self) -> list[T]:
        """
        returns the list of keys in level-order traversal
        """
        if self.empty():
            return []
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append(node.key)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def clear(self):
        """
        delete all nodes from the tree, returns empty instance of TreeNode
        """
        if self.empty():
            return
        stack = [self]
        visited = [False]
        while stack:
            node, vis = stack.pop(), visited.pop()
            if node:
                if vis:
                    node.left = None
                    node.right = None
                else:
                    stack.append(node)
                    visited.append(True)
                    stack.append(node.right)
                    visited.append(False)
                    stack.append(node.left)
                    visited.append(False)
        self.key = None

    def kthLargestElement(self, k: int) -> Union["TreeNode", None]:
        """
        returns k-th biggest element of the tree
        """
        if self.empty():
            return None
        stack = []
        node = self
        while (stack or node) and k > 0:
            if node:
                stack.append(node)
                node = node.right
            else:
                node = stack.pop()
                k -= 1
                if k == 0:
                    return node
                node = node.left
        return None

    def size(self) -> int:
        """
        returns the number of nodes in the tree
        """
        if self.empty():
            return 0
        stack = [self]
        size = 0
        while stack:
            node = stack.pop()
            size += 1
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return size

    def empty(self) -> bool:
        """
        returns True if the size of the tree is equal zero
        """
        return self == TreeNode()

    def elementAccess(self, target_key: T) -> Union[T, None]:
        """
        returns value of the key if exists or it returns None if key does not exist
        """
        if self.empty():
            return None
        current = self
        while current:
            if self.comparator(current.key, target_key) == 0:
                return current.value
            elif self.comparator(current.key, target_key) > 0:
                current = current.left
            else:
                current = current.right
        return None

    def find(self, target_key: T) -> Union["TreeNode", None]:
        """
        returns the node with the specified key or it returns None
        if node does not exist
        """
        if self.empty():
            return None
        current = self
        while current:
            if self.comparator(current.key, target_key) == 0:
                return current
            elif self.comparator(current.key, target_key) > 0:
                current = current.left
            else:
                current = current.right
        return None

    def findmin(self) -> Union[T | None]:
        """
        returns the smallest key, or None if the tree is empty
        """
        if self.empty():
            return None
        node = self
        while node.left:
            node = node.left
        return node.key

    def findmax(self) -> Union[T | None]:
        """
        returns the largest key
        """
        if self.empty():
            return None
        node = self
        while node.right:
            node = node.right
        return node.key

    def previous(self, target: T) -> T:
        """
        returns the in-order predecessor of a given node, if the target
        is lower or equal to minimum key or tree is empty returns None
        """
        if self.empty():
            return None
        current = self
        predecessor = None
        while current:
            if self.comparator(current.key, target) < 0:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    def next(self, target: T) -> T:
        """
        returns the successor of the key in sorted order, if the target
        is greater or equal to maximum key or tree is empty returns None
        """
        if self.empty():
            return None
        current = self
        successor = None
        while current:
            if self.comparator(current.key, target) > 0:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor
