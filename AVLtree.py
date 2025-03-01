from collections import deque
from binarySearchTree import TreeNode
from typing import Any, TypeVar, Union, Callable


T = TypeVar("T")

class AVLtree(TreeNode):
    def __init__(self, key=None, left=None, right=None, value=None, comparator = None):
        super().__init__(key, value, left, right)
        self.height = 1
        self.metaValue = None

    def __repr__(self):
        return super().__repr__()

    def insert(self, new_key: T, new_value: T) -> "AVLtree":
        """
        Inserts a new key-value pair into the AVL tree.
        :param new_key: The key of the new node.
        :param new_value: The value of the new node.
        
        Returns the root of the balanced AVL tree after insertion.
        """
        if self.empty():
            self.key, self.value = new_key, new_value
            return self
        elif self.comparator(self.key, new_key) == 0:
            raise KeyError("The key with the same weight is already in the tree") 
        elif self.comparator(self.key, new_key) > 0:
            if self.left:
                self.left = self.left.insert(new_key, new_value)
            else:
                self.left = AVLtree(key = new_key, value = new_value, comparator = self.comparator)
        else:
            if self.right:
                self.right = self.right.insert(new_key, new_value)
            else:
                self.right = AVLtree(key = new_key, value = new_value, comparator = self.comparator)
        return self.balance()

    def delete(self, key: T) -> "AVLtree":
        """
        Deletes a node with the specified key from the AVL tree.
        
        If the key is found, the node is removed, and the tree is rebalanced to maintain the AVL property.
        If the key is not found, the tree remains unchanged.
        
        :param key:The key of the node to be deleted.

        Returns the root of the balanced AVL tree after deletion. If the tree becomes empty, returns `None`.
        """
        compare_value = self.comparator(self.key, key) 
        if compare_value > 0 and self.left:
            self.left = self.left.delete(key)
        elif compare_value < 0 and self.right:
            self.right = self.right.delete(key)
        elif compare_value == 0:
            if self.left is None and self.right is None:
                return None
            elif self.left is None:
                temp = self.right
                self = None
                return temp
            elif self.right is None:
                temp = self.left
                sef = None
                return temp
            successor = self.next(key)
            self.key, self.value = successor.key, successor.value
            self.right = self.right.delete(successor.key)
        else:
            return self
        return self.balance()
    
    def merge(self, tree1: "AVLtree", tree2: "AVLtree") -> "AVLtree":
        """
        Merges two AVL trees into a single balanced AVL tree.
        
        :param tree1 (AVLtree): The first AVL tree to be merged.
        :param tree2 (AVLtree): The second AVL tree to be merged.

        Returns a new balanced AVL tree containing all key-value pairs from both input trees.
        If both input trees are empty, returns an empty AVL tree.
        """
        in_order_1 = tree1.inorder()
        in_order_2 = tree2.inorder()
        if len(in_order_1) == 0 and len(in_order_2) == 0:
            return AVLtree()
        merged_list = self.mergeList(in_order_1, in_order_2)
        return self.buildTheBalancedTree(merged_list)

    def buildTheBalancedTree(self, sorted_array:list [tuple[T]]) -> "AVLtree":
        """
        Constructs a balanced AVL tree from a sorted array of key-value pairs.
        
        :param sorted_array: A sorted list of tuples, where each tuple contains a key and its
        corresponding value.

        Returns: The root of the newly constructed balanced AVL tree.
        """
        return self.buildTheBalancedTree_helper(sorted_array, 0, len(sorted_array) - 1)
    
    def buildTheBalancedTree_helper(self, sorted_array: list[tuple[T]], start: int, end: int) -> "AVLtree":
        """
        Build the balanced tree from the sorted array. Helper method for buildTheBalancedTree.
        
        :param sorted_array: A sorted list of tuples, where each tuple contains a key and its
        corresponding value.
        :param start: The starting index of the current range in the sorted array.
        :param end: The ending index of the current range in the sorted array.

        """
        if start > end:
            return None
        middle = (start + end) // 2
        node = AVLtree(key = sorted_array[middle][0], value = sorted_array[middle][1])
        node.left = self.buildTheBalancedTree_helper(sorted_array, start, middle - 1)
        node.right = self.buildTheBalancedTree_helper(sorted_array, middle + 1, end)
        self.updateHeight(node)
        return node
    
    @staticmethod
    def mergeList(array1: list[tuple[T]], array2: list[tuple[T]]) -> list[tuple[T]]:
        """
        Merges two sorted lists of key-value pairs into a single sorted list.

        :param array1: The first sorted list of key-value pairs.
        :param array2: The second sorted list of key-value pairs.

        Returns a new sorted list containing all key-value pairs from both input lists,
        with duplicates removed.
        """
        i, j =  0, 0
        result = []
        while i < len(array1) and j < len(array2):
            if array1[i][0] < array2[j][0]:
                result.append(array1[i])
                i += 1
            elif array1[i][0] > array2[j][0]:
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

    def balance(self) -> "AVLtree":
        """
        Balances the AVL tree at the current node.
        """
        self.height = 1 + max(self.getHeight(self.left),
                              self.getHeight(self.right))
        balance_factor = self.getHeight(self.left) - self.getHeight(self.right)
        if balance_factor > 1:
            if self.getHeight(self.left.left) - self.getHeight(self.left.right) < 0:
                self.left = self.left.left_rotate()
            return self.right_rotate()
        elif balance_factor < -1:
            if self.getHeight(self.right.left) - self.getHeight(self.right.right) > 0:
                self.right = self.right.right_rotate()
            return self.left_rotate()
        return self

    def getHeight(self, node:"AVLtree") -> int:
        """
        Returns the height of the given node in the AVL tree. If `None`, the height is 0.
        
        :param node: The node whose height is to be determined. 
        """
        if not node:
            return 0
        return node.height

    def updateHeight(self, node: "AVLtree"):
        """
        Updates the height of the node.

        :param node: Node the height of which will be updated.
        """
        node.height = 1 + max(self.getHeight(self.left), self.getHeight(self.right))

    def right_rotate(self) -> "AVLtree" :
        result = self.left
        left_right_child = result.right
        result.right = self
        self.left = left_right_child
        self.updateHeight(self)
        self.updateHeight(result)
        return result   
    
    def left_rotate(self) -> "AVLtree":
        result = self.right
        right_left_child = result.left
        result.left = self
        self.right = right_left_child
        self.updateHeight(self)
        self.updateHeight(result)
        return result

    def isBalanced(self) -> bool:
        """
        Checks whether the AVL tree is balanced.

        Returns `True` if the tree is balanced, `False` otherwise.
        """
        stack = [self]
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
        
