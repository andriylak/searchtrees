from collections import deque
from typing import Any, TypeVar, Union, Callable
from TreeNode import _TreeNode

T = TypeVar("T")

def sumOfTheValues(left_subtree, right_subtree, value):
    return (left_subtree or 0) + (right_subtree or 0) + value

DEFAULT_METAVALUE_FUNCTION = sumOfTheValues 
DEFAULT_COMPARATOR = lambda a, b: a - b

class BinarySearchTree:
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
        root: Union["_TreeNode", None] = None,
        comparator: Callable[[T], int] | None = None,
    ):
        """
        Initialize a tree root (tree configurations).

        Args:
            root: The root node of the tree. An instance of class _TreeNode.
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
            self.comparator = DEFAULT_COMPARATOR

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

    def __eq__(self: "BinarySearchTree", tree2: "BinarySearchTree") -> bool:
        """
        Returns True if two trees are identical (checks only keys).

        Args:
            tree2 (BinarySearchTree): The root of the tree to compare with.

        Returns:
            bool: True if the trees are identical, False otherwise.

        Raises:
            TypeError: If `tree2` is not an instance of BinarySearchTree
        """
        if not isinstance(tree2, BinarySearchTree):
            raise TypeError(f"Cannot compare BinarySearchTree with {type(tree2).__name__}")
        elif tree2.empty() ^ self.empty():
            return False
        return self.root == tree2.root


    def getMetaValue(self, target_key: T, func: Callable[[T], T] = DEFAULT_METAVALUE_FUNCTION) -> T:
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
            node._metaValue = func(node.left._metaValue if node.left else None,
                                   node.right._metaValue if node.right else None,
                                   node.value)
            if node.left:
                node.left._metaValue = None
            if node.right:
                node.right._metaValue = None
        return target_node._metaValue

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
        Deletes all nodes from the tree and resets the current instance of _TreeNode to an empty state.
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

    def find(self, target_key: T) -> Union["_TreeNode", None]:
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

    def kthLargestElement(self, k: int) -> Union["_TreeNode", None]:
        """
        Returns the k-th largest element in the tree.

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the largest element.

        Returns:
            _TreeNode or None: The k-th largest node, or None if not found.

        Raises:
            TypeError: If `k` is not an integer.
        """
        if not isinstance(k, int):
            raise TypeError(f"The k must be an integer not {type(k).__name__}")
        if not self.empty():
            return self.root.kthLargestElement(k)
        return None

    def kthSmallestElement(self, k: int) -> Union["_TreeNode", None]:
        """
        Finds and returns the k-th smallest element in the binary search tree (BST).

        Args:
            k (int): The position of the desired element in the sorted order of the tree's
                    elements, where 1 corresponds to the smallest element.

        Returns:
            _TreeNode or None: The k-th smallest node, or None if not found.

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
            _TreeNode or None: The smallest key, or None if the tree is empty.
        """
        if not self.empty():
            return self.root.findmin()
        return None

    def findmax(self) -> Union[T, None]:
        """
        Returns the largest key in the tree.

        Returns:
            _TreeNode or None: The largest key, or None if the tree is empty.
        """
        if not self.empty():
            return self.root.findmax()
        return None

    def previous(self, node: "_TreeNode", target: T) -> "_TreeNode":
        """
        Returns the in-order predecessor of a given node.

        Args:
            node (_TreeNode): The root of a tree or subtree in which the predecessor is to be found.
            target: The key for which the in-order predecessor is to be found.

        Returns:
            _TreeNode or None: The in-order predecessor of the target key, or None if the key is a minimum.

        Raises:
            TypeError: If `node` is not an instance of _TreeNode or its subclass.
        """
        if not isinstance(node, _TreeNode):
            raise TypeError(f"The node must be an instance of _TreeNode or its subclass not {type(node).__name__}")
        current = node
        predecessor = None
        while current:
            if self.comparator(current.key, target) < 0:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    def next(self, node: "_TreeNode", target: T) -> "_TreeNode":
        """
        Returns the in-order successor of a given node.

        Args:
            node (_TreeNode): The root of a tree or subtree in which the successor is to be found.
            target: The key for which the in-order successor is to be found.

        Returns:
            _TreeNode or None: The in-order successor of the target key, or None if the key is a maximum.

        Raises:
            TypeError: If `node` is not an instance of _TreeNode or its subclass.
        """
        if not isinstance(node, _TreeNode):
            raise TypeError(f"The node must be an instance of _TreeNode or its subclass not {type(node).__name__}")
        current = node
        successor = None
        while current:
            if self.comparator(current.key, target) > 0:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor
