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
        comparator: Callable[[T], int]| None = None,
    ):
        """
        Initialize a tree node.
        :param key: The key of the node.
        :param value: The value of the node.
        :param left: The left child of the node.
        :param right: The right child of the node.
        :param comparator: Function, which explain how to calculate the weight of the each node.
        """
        self.key = key
        self.value = value
        self.left = left
        self.right = right
        if comparator:
            self.comparator = comparator
            self.setComparator()
        else:
            self.comparator =  lambda a, b: a - b
        self.metaValue = None

    def setComparator(self):
        """
        Sets the comparator function for all nodes in the tree.
        """
        stack = [self]
        while stack:
            node = stack.pop()
            node.comparator = self.comparator
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

    def __iter__(self):
        """
        Returns an iterator that performs an in-order traversal of the tree.
        
        Yields tuple: A (key, value) pair for each node in the tree.
        """
        if self.empty():
            return
        stack = []
        node = self
        while stack or node:
            if node:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                yield (node.key, node.value)
                node = node.right

    def getMetaValue(self, target_key: T, func: Callable[[T], T]) -> T:
        """
        Returns the auxiliary data of the key if exists or it returns None if key does not exist
        :param target_key: The key of the node for which meta value will be calculated.
        :param function:  Function, which explain how to calculate mata value in the each node
        """
        target_node = self.find(target_key)
        if target_node is None:
            return None
        stack = [target_node]
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
        result = node.metaValue
        self.metaValue = None
        return result

    # def comparator(self, value1: T, value2: T) -> int:
    #     """
    #     Compare two keys using calculate_func, which determine the weight of the key.
    #     """
    #     return self.calculate_func(value1) - self.calculate_func(value2)

    def __repr__(self) -> str:
        """
        Returns a string representation of the tree node and its subtrees.
        
        The representation follows the format:
                key (left_subtree) ^ [right_subtree]
        """
        return f"{self.key} ({self.left}) ^ [{self.right}]"

    def __eq__(self, root: "TreeNode") -> bool:
        """
        Returns True if two trees are identical (checks only keys).
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
        Returns the list of tuples (key, key value) in pre-order traversal.
        """
        if self.empty():
            return []
        result = []
        stack = [self]
        while stack:
            node = stack.pop()
            result.append((node.key, node.value))
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    def inorder(self) -> list[T]:
        """
        Returns the list of tuples (key, key value) in in-order traversal.
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
                result.append((node.key, node.value))
                node = node.right
        return result

    def postorder(self) -> list[T]:
        """
        Returns the list of tuples (key, key value) in post-order traversal.
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
                    result.append((node.key, node.value))
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
        Returns the list of tuples (key, key value) in level-order traversal.
        """
        if self.empty():
            return []
        result = []
        queue = deque([self])
        while queue:
            node = queue.popleft()
            result.append((node.key, node.value))
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        return result

    def clear(self):
        """
        Delete all nodes from the tree and resets current instance of TreeNode to an empty state
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
        Returns k-th biggest element of the tree.
        :param k (int): The position of the desired element in the sorted order of the tree's
                elements, where 1 corresponds to the largest element.
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
        Returns the number of nodes in the tree.
        Empty tree has the size 0.
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
        Returns True if the size of the tree is equal zero.
        """
        return self == TreeNode()

    def elementAccess(self, target_key: T) -> Union[T, None]:
        """
        Returns value of the key if exists or it returns None if key does not exist.
        :param target_key: the key to search for in the tree.
        """
        node = self.find(target_key)
        if node is None:
            return None
        return node.value

    def find(self, target_key: T) -> Union["TreeNode", None]:
        """
        Returns the node with the specified key or None if node does not exist.
        :param target_key: the key to search for in the tree.
        """
        if self.empty():
            return None
        current = self
        while current:
            if self.comparator(current.key, target_key) == 0: 
                if current.key == target_key:
                    return current
                else:
                    return None                                          # can't be two nodes with the same weight inside the tree
            elif self.comparator(current.key, target_key) > 0:
                current = current.left
            else:
                current = current.right
        return None

    def findmin(self) -> Union[T | None]:
        """
        Returns the smallest key, or None if the tree is empty.
        """
        if self.empty():
            return None
        node = self
        while node.left:
            node = node.left
        return node.key

    def findmax(self) -> Union[T | None]:
        """
        Returns the largest key, or None if the tree is empty.
        """
        if self.empty():
            return None
        node = self
        while node.right:
            node = node.right
        return node.key

    def previous(self, target: T) -> T:
        """
        Returns the in-order predecessor of a given node, if the target
        is lower or equal to minimum key or tree is empty returns None.
        :param target: the key for which the in-order predecessor is to be found.
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
        Returns the successor of the key in sorted order, if the target
        is greater or equal to maximum key or tree is empty returns None.
        :param target: the key for which the in-order successor is to be found.
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
