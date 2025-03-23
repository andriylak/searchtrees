from collections import deque
import queue
from typing import Any, TypeVar, Union, Callable

T = TypeVar("T")

class TreeNode:
    """
    A class representing a node in a tree structure.

    Each node contains a key, a value, and references to its left and right children.
    Additional metadata, such as `metaValue`, can also be stored for advanced tree operations.

    Attributes:
        key: The key associated with the node. Defaults to None.
        value: The value stored in the node. Defaults to None.
        left: The left child of the node. Defaults to None.
        right: The right child of the node. Defaults to None.
        metaValue: Optional metadata associated with the node. Defaults to None.
    """

    def __init__(
        self,
        key: Union[T, None] = None,
        value: Union[T, None] = None,
        left: Union["TreeNode", None] = None,
        right: Union["TreeNode", None] = None,
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
        self.metaValue = None

    def __repr__(self) -> str:
        """
        Returns a string representation of the tree node and its subtrees.

        The representation follows the format:
            key (left_subtree) ^ [right_subtree]

        Returns:
            str: A string representation of the tree node.
        """
        return f"{self.key} ({self.left}) ^ [{self.right}]"

    def __eq__(self: "TreeNode", root: "TreeNode") -> bool:
        """
        Returns True if two trees are identical (checks only keys).

        Args:
            root (TreeNode): The root of the tree to compare with.

        Returns:
            bool: True if the trees are identical, False otherwise.

        Raises:
            TypeError: If `root` is not an instance of TreeNode.
        """
        if not isinstance(root, TreeNode):
            raise TypeError(f"Cannot compare TreeNode with {type(root).__name__}")
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

    def preorder(self) -> "TreeNode":
        """
        Performs a pre-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            TreeNode: Each node in the tree in pre-order traversal.
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

    def inorder(self) -> "TreeNode":
        """
        Performs an in-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            TreeNode: Each node in the tree in in-order traversal.
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

    def reverseorder(self) -> "TreeNode":
        """
        Performs a reverse-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            TreeNode: Each node in the tree in reverse-order traversal.
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

    def postorder(self) -> "TreeNode":
        """
        Performs a post-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            TreeNode: Each node in the tree in post-order traversal.
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

    def levelorder(self) -> "TreeNode":
        """
        Performs a level-order traversal of the binary tree and yields each node in traversal order.

        Yields:
            TreeNode: Each node in the tree in level-order traversal.
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

    def kthLargestElement(self, k: int) -> Union["TreeNode", None]:
        """
        Returns the k-th largest element in the tree.

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the largest element.

        Returns:
            TreeNode or None: The k-th largest node, or None if k is bigger than the size of tree.

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

    def kthSmallestElement(self, k: int) -> Union["TreeNode", None]:
        """
        Finds and returns the k-th smallest element in the binary search tree (BST).

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the smallest element.

        Returns:
            TreeNode or None: The k-th smallest node, or None if k is bigger than the size of tree.

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

class TreeRoot:
    """
    A class representing the root of a tree structure.

    This class serves as the entry point for a tree, holding a reference to the root node
    and an optional comparator function for node comparisons. If no comparator is provided,
    a default comparator is used that subtracts the second argument from the first.

    Attributes:
        root: The root node of the tree. Defaults to None if the tree is empty.
        comparator: A function to compare two nodes. If not provided,
            a default comparator is used that subtracts the second argument from the first.
    """

    def __init__(
        self,
        root: Union["TreeNode", None] = None,
        comparator: Callable[[T], int] | None = None,
    ):
        """
        Initialize a tree root (tree configurations).

        Args:
            root: The root node of the tree. An instance of class TreeNode.
                Defaults to None if the tree is empty.
            comparator: A function to compare two keys. If not provided,
                a default comparator is used that subtracts the second argument from the first.

        The comparator function should return:
            - A value greater than 0 if the first key's weight is greater than the second.
            - A value less than 0 if the second key's weight is greater than the first.
            - 0 if the weights of both keys are equal.
        """
        self.root = root
        if comparator:
            self.comparator = comparator
        else:
            self.comparator = lambda a, b: a - b

    def __iter__(self):
        """
        Returns an iterator that performs an in-order traversal of the tree.

        Yields:
            tuple: A (key, value) pair for each node in the tree.
        """
        if self.empty():
            return iter([])
        for node in self.root.inorder():
            yield (node.key, node.value)

    def __repr__(self):
        """
        Returns a string representation of the tree node and its subtrees.

        Returns:
            str: A string representation of the tree.
        """
        return f"{{ {self.root} }}"

    def __eq__(self: "TreeRoot", tree2: "TreeRoot") -> bool:
        """
        Returns True if two trees are identical (checks only keys).

        Args:
            tree2 (TreeRoot): The root of the tree to compare with.

        Returns:
            bool: True if the trees are identical, False otherwise.

        Raises:
            TypeError: If `tree2` is not an instance of TreeRoot
        """
        if not isinstance(tree2, TreeRoot):
            raise TypeError(f"Cannot compare TreeRoot with {type(tree2).__name__}")
        elif tree2.empty() ^ self.empty():
            return False
        return self.root == tree2.root


    def getMetaValue(self, target_key: T, func: Callable[[T], T]) -> T:
        """
        Returns the auxiliary data of the key if it exists, or None if the key does not exist.

        Args:
            target_key: The key of the node for which the meta value will be calculated.
            func: A function that explains how to calculate the meta value for each node.

        Returns:
            The meta value of the target key, or None if the key does not exist.
        """
        target_node = self.find(target_key)
        if target_node is None:
            return None
        for node in target_node.postorder():
            node.metaValue = func(
                left_subtree=node.left.metaValue if node.left else None,
                right_subtree=node.right.metaValue if node.right else None,
                node_value=node.value,
            )
            if node.left:
                node.left.metaValue = None
            if node.right:
                node.right.metaValue = None
        return target_node.metaValue

    def getPreorder(self) -> list[tuple[T]]:
        """
        Returns a list of tuples containing the (key, value) pairs of all nodes in the tree,
        obtained through a pre-order traversal.

        Returns:
            list: A list of (key, value) pairs in pre-order traversal.
        """
        result = []
        if not self.empty():
            for node in self.root.preorder():
                result.append((node.key, node.value))
        return result

    def getInorder(self) -> list[tuple[T]]:
        """
        Returns a list of tuples containing the (key, value) pairs of all nodes in the tree,
        obtained through an in-order traversal.

        Returns:
            list: A list of (key, value) pairs in in-order traversal.
        """
        result = []
        if not self.empty():
            for node in self.root.inorder():
                result.append((node.key, node.value))
        return result

    def getReverseorder(self) -> list[tuple[T]]:
        """
        Returns a list of tuples containing the (key, value) pairs of all nodes in the tree,
        obtained through a reverse-order traversal.

        Returns:
            list: A list of (key, value) pairs in reverse-order traversal.
        """
        result = []
        if not self.empty():
            for node in self.root.reverseorder():
                result.append((node.key, node.value))
        return result

    def getPostorder(self) -> list[tuple[T]]:
        """
        Returns a list of tuples containing the (key, value) pairs of all nodes in the tree,
        obtained through a post-order traversal.

        Returns:
            list: A list of (key, value) pairs in post-order traversal.
        """
        result = []
        if not self.empty():
            for node in self.root.postorder():
                result.append((node.key, node.value))
        return result

    def getLevelorder(self) -> list[tuple[T]]:
        """
        Returns a list of tuples containing the (key, value) pairs of all nodes in the tree,
        obtained through a level-order traversal.

        Returns:
            list: A list of (key, value) pairs in level-order traversal.
        """
        result = []
        if not self.empty():
            for node in self.root.levelorder():
                result.append((node.key, node.value))
        return result

    def clear(self) -> None:
        """
        Deletes all nodes from the tree and resets the current instance of TreeNode to an empty state.
        """
        if self.empty():
            return
        for node in self.root.postorder():
            node.key = None
            node.value = None
            node.left = None
            node.right = None
        self.root = None

    def size(self) -> int:
        """
        Returns the number of nodes in the tree.

        Returns:
            int: The number of nodes in the tree. An empty tree has a size of 0.
        """
        if self.empty():
            return 0
        return self.root.size()

    def empty(self) -> bool:
        """
        Returns True if the size of the tree is equal to zero.

        Returns:
            bool: True if the tree is empty, False otherwise.
        """
        if self.root is None:
            return True
        return False

    def elementAccess(self, target_key: T) -> Union[T, None]:
        """
        Returns the value of the key if it exists, or None if the key does not exist.

        Args:
            target_key: The key to search for in the tree.

        Returns:
            Key or None: The value of the key, or None if the key does not exist.

        Raises:
            KeyError: If the given key does not exist in the tree.
        """
        node = self.find(target_key)
        if node is None:
            raise KeyError(f"The key {target_key} doesn't exist inside the tree")
        return node.value

    def find(self, target_key: T) -> Union["TreeNode", None]:
        """
        Returns the node with the specified key or None if the node does not exist.

        Args:
            target_key (T): The key to search for in the tree.

        Returns:
            Key or None: The node with the specified key, or None if not found.
        """
        if self.empty():
            return None
        current = self.root
        while current:
            if self.comparator(current.key, target_key) == 0:
                if current.key == target_key:
                    return current
                else:
                    return None                                               # Can't be two nodes with the same weight inside the tree
            elif self.comparator(current.key, target_key) > 0:
                current = current.left
            else:
                current = current.right
        return None

    def kthLargestElement(self, k: int) -> Union["TreeNode", None]:
        """
        Returns the k-th largest element in the tree.

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the largest element.

        Returns:
            TreeNode or None: The k-th largest node, or None if not found.

        Raises:
            TypeError: If `k` is not an integer.
        """
        if not isinstance(k, int):
            raise TypeError(f"The k must be an integer not {type(k).__name__}")
        if not self.empty():
            return self.root.kthLargestElement(k)
        return None

    def kthSmallestElement(self, k: int) -> Union["TreeNode", None]:
        """
        Finds and returns the k-th smallest element in the binary search tree (BST).

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the smallest element.

        Returns:
            TreeNode or None: The k-th smallest node, or None if not found.

        Raises:
            TypeError: If `k` is not an integer.
        """
        if not isinstance(k, int):
            raise TypeError(f"The k must be an integer not {type(k).__name__}")
        if not self.empty():
            return self.root.kthSmallestElement(k)
        return None

    def findmin(self) -> Union[T, None]:
        """
        Returns the smallest key in the tree.

        Returns:
            TreeNode or None: The smallest key, or None if the tree is empty.
        """
        if not self.empty():
            return self.root.findmin()
        return None

    def findmax(self) -> Union[T, None]:
        """
        Returns the largest key in the tree.

        Returns:
            TreeNode or None: The largest key, or None if the tree is empty.
        """
        if not self.empty():
            return self.root.findmax()
        return None

    def previous(self, node: "TreeNode", target: T) -> "TreeNode":
        """
        Returns the in-order predecessor of a given node.

        Args:
            node (TreeNode): The root of a tree or subtree in which the predecessor is to be found.
            target: The key for which the in-order predecessor is to be found.

        Returns:
            TreeNode or None: The in-order predecessor of the target key, or None if the key is a minimum.

        Raises:
            TypeError: If `node` is not an instance of TreeNode or its subclass.
        """
        if not isinstance(node, TreeNode):
            raise TypeError(f"The node must be an instance of TreeNode or its subclass not {type(node).__name__}")
        current = node
        predecessor = None
        while current:
            if self.comparator(current.key, target) < 0:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    def next(self, node: "TreeNode", target: T) -> "TreeNode":
        """
        Returns the in-order successor of a given node.

        Args:
            node (TreeNode): The root of a tree or subtree in which the successor is to be found.
            target: The key for which the in-order successor is to be found.

        Returns:
            TreeNode or None: The in-order successor of the target key, or None if the key is a maximum.

        Raises:
            TypeError: If `node` is not an instance of TreeNode or its subclass.
        """
        if not isinstance(node, TreeNode):
            raise TypeError(f"The node must be an instance of TreeNode or its subclass not {type(node).__name__}")
        current = node
        successor = None
        while current:
            if self.comparator(current.key, target) > 0:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor
