from binarySearchTree import DEFAULT_COMPARATOR, TreeRoot, TreeNode
from typing import Any, TypeVar, Union, Callable
from functools import cmp_to_key, partial


T = TypeVar("T")

def first_element_comparator(comparator: Callable[[T], int], a: tuple, b: tuple)->int:
     """
     A comparator function that compares the first elements of two tuples.
     """
     return comparator(a[0], b[0])

class AVLTreeNode(TreeNode):
    """
    A class representing a node in an AVL tree.

    This class extends the TreeNode class to include height information for balancing.

    Attributes:
        key: The key of the node.
        value: The value of the node.
        left: The left child of the node.
        right: The right child of the node.
        metaValue: Optional metadata associated with the node.
        height (int): The height of the node in the AVL tree.
    """
    def __init__(
        self,
        key: Union[T , None] = None,
        value: Union [T , None] = None,
        left: Union["TreeNode" , None] = None,
        right: Union["TreeNode" , None] = None,
    ):
        """
        Initialize an AVL tree node.

        Args:
            key: The key of the node.
            value: The value of the node.
            left: The left child of the node.
            right: The right child of the node.
        """
        super().__init__(key, value, left, right)
        self.height = 1

class AVLtree(TreeRoot):
    """
    A class representing an AVL tree, a self-balancing binary search tree.

    This class extends the TreeRoot class to provide AVL tree functionality, including
    insertion, deletion, and balancing operations.

    Attributes:
        root (Union[TreeNode, None]): The root node of the AVL tree.
        comparator (Callable[[T], int]): A function to compare two keys.
        metaValue (Any): Optional metadata associated with the tree.
    """

    def __init__(self, root: Union["TreeNode", None] = None, comparator: Callable[[T], int] | None = None):
        """
        Initialize an AVL tree.

        Args:
            root: The root node of the AVL tree.
            comparator: A function to compare two keys.
        """
        super().__init__(root, comparator)

    def insert(self, new_key: T, new_value: T) -> "AVLtree":
        """
        Inserts a new key-value pair into the AVL tree.

        Args:
            new_key: The key of the new node.
            new_value: The value of the new node.

        Returns:
            AVLtree: The root of the balanced AVL tree after insertion.
        """
        if self.empty():
            self.root = AVLTreeNode(new_key, new_value)
        else:
            self.root = self._insert_recursive(self.root, new_key, new_value)
    
    def _insert_recursive(self, node: "TreeNode", new_key: T, new_value: T) -> "AVLTreeNode":
        """
        Helper method. Recursively inserts a new key-value pair into the AVL tree.

        Args:
            node (AVLTreeNode): The current node in the recursion.
            new_key: The key of the new node.
            new_value: The value of the new node.

        Returns:
            AVLTreeNode: The root of the balanced subtree after insertion.
        """
        if not node:
            return AVLTreeNode(new_key, new_value)
        elif self.comparator(node.key, new_key) == 0:
            return node
        elif self.comparator(node.key, new_key) > 0:
            node.left = self._insert_recursive(node.left, new_key, new_value)
        else:
            node.right = self._insert_recursive(node.right, new_key, new_value)
        return self._balance(node)

    def delete(self, key: T) -> "AVLtree":
        """
        Deletes a node with the specified key from the AVL tree.

        Args:
            key (T): The key of the node to be deleted.

        Returns:
            AVLtree: The root of the balanced AVL tree after deletion.
        """
        if self.empty():
            pass
        else:
            self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node: "TreeNode", key: T) -> "AVLTreeNode":
        """
        Recursively deletes a node with the specified key from the AVL tree.

        Args:
            node (AVLTreeNode): The current node in the recursion.
            key: The key of the node to be deleted.

        Returns:
            TreeNode: The root of the balanced subtree after deletion.
        """
        if not node:
            return node
        elif self.comparator(node.key, key) > 0:
            node.left = self._delete_recursive(node.left, key)
        elif self.comparator(node.key, key) < 0:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                temp = node.right
                node = None
                return temp
            elif node.right is None:
                temp = node.left
                node = None
                return temp
            successor = self.next(node, key)
            node.key, node.value = successor.key, successor.value
            node.right = self._delete_recursive(node.right, successor.key)
        if not node:
            return node
        return self._balance(node)

    def merge(self, tree1: "AVLtree", tree2: "AVLtree") -> "AVLtree":
        """
        Merges two AVL trees into a single balanced AVL tree.

        Args:
            tree1 (AVLtree): The first AVL tree to be merged.
            tree2 (AVLtree): The second AVL tree to be merged.

        Returns:
            AVLtree: A new balanced AVL tree containing all key-value pairs from both input trees. The 
            comparator of a new tree is the same with the comparator in tree1.
        """
        merged_tree = AVLtree(comparator=tree1.comparator)
        for (key, value) in tree1:
            merged_tree.insert(key, value)
        for (key, value) in tree2:
            merged_tree.insert(key, value)
        return merged_tree

    def buildTheBalancedTree(self, array: list[tuple[T]], comparator:Callable[[T], int] = DEFAULT_COMPARATOR, isSorted:bool = False) -> "AVLtree":
        """
        Constructs a balanced AVL tree from a sorted array of key-value pairs.

        Args:
            array: A list of tuples, where each tuple contains a key and its corresponding value.
            comparator (Callable): The comparator function to use for key comparisons.
            sorted(bool): Indicator, which tells whether the input is sorted according to comparator rules,
              is False by default.

        Returns:
            AVLtree: The root of the newly constructed balanced AVL tree.
        """
        if not isSorted:
            custom_comparator = cmp_to_key(partial(first_element_comparator, comparator))
            array = sorted(array, key=custom_comparator)
        start, end = 0, len(array) - 1
        middle = (start + end) // 2
        tree = AVLtree(comparator=comparator)
        tree.root = AVLTreeNode(key=array[middle][0], value=array[middle][1])
        tree.root.left = self._buildTheBalancedTree_helper(array, start, middle - 1)
        tree.root.right = self._buildTheBalancedTree_helper(array, middle + 1, end)
        self._updateHeight(tree.root)
        return tree

    def _buildTheBalancedTree_helper(self, sorted_array: list[tuple[T]], start: int, end: int) -> "AVLTreeNode":
        """
        Helper method for building a balanced AVL tree from a sorted array.

        Args:
            sorted_array: A sorted list of tuples, where each tuple contains a key and its corresponding value.
            start (int): The starting index of the current range in the sorted array.
            end (int): The ending index of the current range in the sorted array.

        Returns:
            AVLTreeNode: The root of the balanced subtree.
        """
        if start > end:
            return None
        middle = (start + end) // 2
        node = AVLTreeNode(key=sorted_array[middle][0], value=sorted_array[middle][1])
        node.left = self._buildTheBalancedTree_helper(sorted_array, start, middle - 1)
        node.right = self._buildTheBalancedTree_helper(sorted_array, middle + 1, end)
        self._updateHeight(node)
        return node

    @staticmethod
    def mergeList(array1: list[tuple[T]], array2: list[tuple[T]], comparator: Callable[[T], int]) -> list[tuple[T]]:
        """
        Merges two sorted lists of key-value pairs into a single sorted list.

        Args:
            array1: The first sorted list of key-value pairs.
            array2: The second sorted list of key-value pairs.
            comparator (Callable): The comparator function to use for key comparisons.

        Returns:
            list: A new sorted list containing all key-value pairs from both input lists.
        """
        i, j = 0, 0
        result = []
        while i < len(array1) and j < len(array2):
            if comparator(array1[i][0], array2[j][0]) < 0:
                result.append(array1[i])
                i += 1
            elif comparator(array1[i][0], array2[j][0]) > 0:
                result.append(array2[j])
                j += 1
            else:
                result.append(array1[i])
                i += 1
                j += 1
        if i < len(array1):
            result = result + array1[i:]
        if j < len(array2):
            result = result + array2[j:]
        return result

    def _balance(self, node: "AVLTreeNode") -> "AVLTreeNode":
        """
        Balances the AVL tree at the current node.

        Args:
            node (AVLTreeNode): The node to balance.

        Returns:
            AVLTreeNode: The root of the balanced subtree.
        """
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        balance_factor = self.getHeight(node.left) - self.getHeight(node.right)
        if balance_factor > 1:
            if self.getHeight(node.left.left) - self.getHeight(node.left.right) < 0:
                node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        elif balance_factor < -1:
            if self.getHeight(node.right.left) - self.getHeight(node.right.right) > 0:
                node.right = self._right_rotate(node.right)
            return self._left_rotate(node)
        return node

    def getHeight(self, node: "AVLTreeNode") -> int:
        """
        Returns the height of the given node in the AVL tree.

        Args:
            node (AVLTreeNode): The node whose height is to be determined.

        Returns:
            int: The height of the node. If the node is `None`, returns 0.
        """
        if not node:
            return 0
        return node.height

    def _updateHeight(self, node: "AVLTreeNode"):
        """
        Updates the height of the node.

        Args:
            node (AVLTreeNode): The node whose height is to be updated.
        """
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

    def _right_rotate(self, node: "TreeNode") -> "AVLtree":
        """
        Performs a right rotation on the given node.

        Args:
            node (TreeNode): The node to rotate.

        Returns:
            TreeNode: The new root of the subtree after rotation.
        """
        result = node.left
        left_right_child = result.right
        result.right = node
        node.left = left_right_child
        self._updateHeight(node)
        self._updateHeight(result)
        return result

    def _left_rotate(self, node:"TreeNode") -> "AVLtree":
        """
        Performs a left rotation on the given node.

        Args:
            node (TreeNode): The node to rotate.

        Returns:
            TreeNode: The new root of the subtree after rotation.
        """
        result = node.right
        right_left_child = result.left
        result.left = node
        node.right = right_left_child
        self._updateHeight(node)
        self._updateHeight(result)
        return result

    def isBalanced(self) -> bool:
        """
        Checks whether the AVL tree is balanced.

        Returns:
            bool: `True` if the tree is balanced, `False` otherwise.
        """
        stack = [self.root]
        while stack:
            node = stack.pop()
            balance_factor = self.getHeight(node.left) - self.getHeight(node.right)
            if balance_factor > 1 or balance_factor < -1:
                return False
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return True
