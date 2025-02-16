from collections import deque


class BinarySearchTree:
    def __init__(self, value = None, left = None, right = None):
        self.value = value
        self.left = left
        self.right = right

class AVLTree:
    
    def __init__(self, key, value, auxiliary_data, left = None, right = None):
        self.key = key
        self.value = value 
        self.left = left
        self.right = right

    def preorder(self):
        if self == None:
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

    def inorder(self):
        if self == None:
            return []
        result = []
        stack = []
        node = self
        while stack or node != None:
            if node != None:
                stack.append(node)
                node = node.left
            else:
                node = stack.pop()
                result.append(node.key)
                node = node.right
        return result

    def postorder(self):
        if self == None:
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
                    stack.append(node.left)
                    visited.append(False)
                    stack.append(node.right)
                    visited.append(False)
        return result
    
    def levelorder(self):
        if self == None:
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
        
    # returns the number of nodes in the tree.
    def size(self):
        stack = [self]
        size = 0
        if self == None:
            return 0
        while stack:
            node = stack.pop()
            size += 1
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        return size

    # returns True if the size of the tree is equal zero.
    def empty(self):
        if self != None:
            return True
        return False

    # returns value of the key if exists or it returns None if key does not exist
    def elementAccess(self, target_key):
        current = self
        while current != None:
            if current.key == target_key:
                return current.value
            elif current.key > target_key:
                current = current.left
            else:
                current = current.right
        return None

    # returns the node with the specified key or it returns None if node does not exist
    def find(self, target_key):
        current = self
        while current != None:
            if current.key == target_key:
                return current
            elif current.key > target_key:
                current = current.left
            elif current.key < target_key:
                current = current.right
        return None

    
    # return the smallest key
    def findmin(self):                    
        node = self
        while node.left:
            node = node.left
        return node.key
    
    # return the largest key
    def findmax(self):
        node = self
        while node.right:
            node = node.right
        return node.key

    # returns the in-order predecessor of a given node
    def previous(self, target):
        current = self
        predecessor = None
        while current != None:
            if current.key < target:
                predecessor = current
                current = current.right
            else:
                current = current.left
        return predecessor

    # returns the successor of the key in sorted order.
    def next(self, target):
        current = self
        successor = None
        while current != None:
            if current.key > target:
                successor = current
                current = current.left
            else:
                current = current.right
        return successor

            
    def insert(self, key, value):

    def delete(self, key, value):
