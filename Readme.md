# Documentation for AVL Tree Implementation

## Introduction

Search trees are foundational data structures that organize data in sorted order while maintaining efficient insertion, deletion, and lookup operations. These trees include binary (e.g., `AVL`, `red-black`, `treap`, `splay`) and non-binary (e. g. `2-3 tree`). The project aims to implement these types of trees and create Python library that provides a unified interface for operations on these tree types.

So far, the project contains the `AVL tree` implementation, along with the superclasses `TreeNode` and `TreeRoot`, which include methods that are common to all binary trees.
## File Structure


The project consists of two main files:

1. **`binarySearchTree.py`**: This file contains the base classes `TreeNode` and `TreeRoot`, which provide the foundational structure for binary search trees. It includes methods for tree traversal, node manipulation, and basic tree operations.

2. **`AVLtree.py`**: This file extends the `TreeNode` and `TreeRoot` classes from `binarySearchTree.py` to implement an AVL Tree. It includes methods for balancing the tree, inserting and deleting nodes, and merging trees.

3. **`binarySearchTree_test.py`**: This file contains `unittests` for classes `TreeNode` and `TreeRoot` with `DEFAULT_COMPARATOR`.

4. **`comparator_test`**: This file contains `unittests` for classes `TreeNode` and `TreeRoot` with `custom_comparator`.

5. **`AVLtree_test`**: This file contains `unittests` for `AVLtree` class, including balancing, insert, delete and merge operations.

# Classes and Methods

## `TreeNode` Class (from `binarySearchTree.py`)

The `TreeNode` class represents a node in a binary tree. Each node contains a key, a value, and references to its left and right children. It also includes optional metadata (`metaValue`), which is used for calculating auxiliary data in some node.

#### Attributes:
- **key**: The key associated with the node. Defaults to None
- **value**: The value stored in the node. Defaults to None
- **left**: The left child of the node. Defaults to None
- **right**: The right child of the node. Defaults to None
- **_metaValue**: An internal atribute. Optional metadata associated with the node.

### Methods:
- Each example demonstrates the usage of the method with a consistent tree structure:
  ```
      3
     / \
    1   5
     \ /
     2 4
  ```

#### **`__init__(key = None, value = None, left = None, right = None)`**  
Constructor. Initializes a tree node with a key, value, and optional left and right children. All attributes default to `None`.  

---

#### **`__repr__()`**  
Returns a string representation of the tree node and its subtrees.  

_**The representation follows the format**_:  
```
key:value (left_subtree) ^ [right_subtree]
```
**_Example_** of usage:
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
print(tree)
# Output: 3:C (1:A (None) ^ [2:B]) ^ [5:E (4:D) ^ [None]]

```  

---

#### **`__eq__(node)`**  
Compares two nodes for equality based on their keys. Returns `True` if the trees are identical, `False` otherwise.  Raises `TypeError` if `node` is not an instance of TreeNode.

**_Example_** of usage:  

```python
T = TreeNode
root1 = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
root2 = T(3, value="q", left=T(1, value="w", right=T(2, value="e")), right=T(5, value="r", left=T(4, value="t")))
tree1 = TreeRoot(root1)
tree2 = TreeRoot(root2)
print(tree1 == tree2)  # Output: True
```


---
### Traversals 
>All traversals were implemented using iterative algorithms instead of recursive ones    because not all trees that this project aims to implement are balanced (for example, splay trees). If we used      recursive algorithms, we would almost certainly encounter a `StackOverflow` error when  attempting to traverse a large unbalanced tree. By using iterative algorithms, we       avoid this issue entirely. Nevertheless, we will use recursive algorithms for balanced  trees 
---
#### **`preorder()`**  
Generator. Performs a pre-order traversal of the tree. Yields each node in the tree in pre-order traversal (root → left subtree → right subtree).  
**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
for node in root.preorder():
    print(node.key, end=" ")
# Output: 3 1 2 5 4
```

---

#### **`inorder()`**  
Generator. Performs an in-order traversal of the tree. Yields each node in the tree in in-order traversal (left subtree → root → right subtree).  
**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
for node in root.inorder():
    print(node.key, end=" ")
# Output: 1 2 3 4 5
```

---

#### **`reverseorder()`**  
Generator. Performs a reverse-order traversal of the tree. Yields each node in the tree in reverse-order traversal (right subtree → root → left subtree).  

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
for node in root.reverseorder():
    print(node.key, end=" ")
# Output: 5 4 3 2 1
```

---

#### **`postorder()`**  
Generator. Performs a post-order traversal of the tree. Yields each node in the tree in post-order traversal (left subtree → right subtree → root).  

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
for node in root.postorder():
    print(node.key, end=" ")
# Output: 2 1 4 5 3
```

---

#### **`levelorder()`**  
Generator. Performs a level-order traversal of the tree. Yields each node in the tree in level-order traversal (nodes are visited level by level, from left to right).  

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
for node in root.levelorder():
    print(node.key, end=" ")
# Output: 3 1 5 2 4
```

---



#### **`kthLargestElement(k)`**  
`k` (int): The position of the desired element in the sorted order of the tree's elements, where 1 corresponds to the largest element.

Returns the k-th largest element in the tree. Raises `TypeError`, if `k` is not an integer. 

**Algorithm**: Returns k-th element in `reverseorder()` traversal.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
kth_largest = root.kthLargestElement(2)
print(kth_largest.key)  # Output: 4
```

---

#### **`kthSmallestElement(k)`**  
`k` (int): The position of the desired element in the sorted order of the tree's elements, where 1 corresponds to the smallest element.

Returns the k-th smallest element in the tree. Raises `TypeError`, if `k` is not an integer.

**Algorithm**: Returns k-th element in `inorder()` traversal.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
kth_smallest = root.kthSmallestElement(3)
print(kth_smallest.key)  # Output: 3
```

---

#### **`findmin()`**  
Returns the smallest key in the tree.  

**Algorithm**: Returns the key of `kthSmallestElement(1)` node.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
min_key = root.findmin()
print(min_key)  # Output: 1
```

---

#### **`findmax()`**  
Returns the largest key in the tree.  

**Algorithm**: Returns the key of `kthLargestElement(1)` node.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
max_key = root.findmax()
print(max_key)  # Output: 5
```

---

#### **`size()`**  
Returns the number of nodes in the tree.  

**Algorithm**: Traverses the tree in `inorder()` traversal, and count the nodes

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree_size = root.size()
print(tree_size)  # Output: 5
```

---


## `TreeRoot` Class (from `binarySearchTree.py`)

The `TreeRoot` class represents the root of a tree structure. It holds a reference to the root node and an optional comparator function for node comparisons and building the tree.

#### Attributes:
- **root**: The root node of the tree. This attribute must be an instance of `TreeNode` or its subclass. Defaults to `None`.
- **comparator**: A function to compare two keys. 

#### Comparator

**The comparator function must be strictly defined**.
```python
def comparator_function(key1, key2):
    compare_value = someOperations(key1, key2)
    return compare_value
```
The comparator function should return:
- `compare value > 0` if the first key's weight is greater than the second.
- `compare_value < 0` if the second key's weight is greater than the first.
- `compare_value = 0` if the weights of both keys are equal.

Comparator defaults to DEFAULT_COMPARATOR:

```python
DEFAULT_COMPARATOR = lambda a, b: a - b
```

### Methods
---
- Each example demonstrates the usage of the method with a consistent tree structure:
  ```
      3
     / \
    1   5
     \ /
     2 4
  ```

#### **`__init__(root = None, comparator= None)`**  
Constructor. Initializes a tree root with an optional root node and comparator function.  

---

#### **`__iter__()`**  
Returns an iterator that performs an in-order traversal of the tree. Yields (key, value) pairs for each node.  

**Implementation**: Uses the implementation of `inorder()` traversal in `TreeNode` class.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
for key, value in tree:
    print(f"{key}:{value}", end=" ")
# Output: 1:A 2:B 3:C 4:D 5:E
```

---

#### **`__repr__()`**  
Returns a string representation of the tree node and its subtrees.  

_**The representation follows the format**_:  
```
{tree.root} 
```
But `tree.root` is an instance of `TreeNode`, so the output string would look like:
```
{key:value (left_subtree) ^ [right_subtree]}
```
**_Example_** of usage:

```
key:value (left_subtree) ^ [right_subtree] 
**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
print(tree)
# Output: { 3:C (1:A (None) ^ [2:B]) ^ [5:E (4:D) ^ [None]] }
```

---

#### **`__eq__(tree)`**  
Compares two trees for equality based on their keys. Returns `True` if the trees are identical, `False` otherwise. Raises `TypeError` if `tree` is not an instance of TreeRoot.

**Implementation**: Returns the result of comparison of `root` attributes of trees (instances of `TreeNode`)

**_Example_** of usage:  

```python
T = TreeNode
root1 = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
root2 = T(3, value="q", left=T(1, value="w", right=T(2, value="e")), right=T(5, value="r", left=T(4, value="t")))
tree1 = TreeRoot(root1)
tree2 = TreeRoot(root2)
print(tree1 == tree2)  # Output: True
```

---

#### **`getMetaValue(target_key, func)`**

Returns the `_metaValue` of the key if the key exists, or `None` if the key does not exist. 

`target_key`: The key of the node for which the meta value will be calculated.

`func`: A function that explains how to calculate the meta value for each node.

**Implementation**: Traverse the tree in `postorder()` traversal, and gradually find the value of all nodes below the `target_key`.

**The func must be strictly defined**:
 - The order of arguments inside the `func` definition should be: `left_subtree`, `right_subtree`, `value_of the current node`.
 - Inside the `func` should be defined what to do if the node don't have left_subtree, or right_subtree (or in other case, don't use the `left_subtree` and `right_subtree` in the calculations of `_metaValue`).

**_Example_** of a `func`:
```python
def f(left_subtree, right_subtree, node_value):
    return (right_subtree or '') + (node_value or '') + (left_subtree or '') 
```
**_Example_** of usage:

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
meta_value = tree.getMetaValue(3, lambda left, right, value: value.upper())
print(meta_value)  # Output: C
```

---

#### **`getPreorder()`**  
Returns a list of (key, value) pairs in pre-order traversal.  

**Implementation**: Calls `preorder()` traversal on `root` attribute, and append `(key, value)` pairs to the list.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
preorder = tree.getPreorder()
print(preorder)  # Output: [(3, 'C'), (1, 'A'), (2, 'B'), (5, 'E'), (4, 'D')]
```

---

#### **`getInorder()`**  

Returns a list of (key, value) pairs in in-order traversal.  

**Implementation**: Calls `inorder()` traversal on `root` attribute, and append `(key, value)` pairs to the list.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
inorder = tree.getInorder()
print(inorder)  # Output: [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]
```

---

#### **`getReverseorder()`**  

Returns a list of (key, value) pairs in reverse-order traversal.

**Implementation**: Calls `reverseorder()` traversal on `root` attribute, and append `(key, value)` pairs to the list.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
reverseorder = tree.getReverseorder()
print(reverseorder)  # Output: [(5, 'E'), (4, 'D'), (3, 'C'), (2, 'B'), (1, 'A')]
```

---

#### **`getPostorder()`**  

Returns a list of (key, value) pairs in post-order traversal.  

**Implementation**: Calls `postorder()` traversal on `root` attribute, and append `(key, value)` pairs to the list.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
postorder = tree.getPostorder()
print(postorder)  # Output: [(2, 'B'), (1, 'A'), (4, 'D'), (5, 'E'), (3, 'C')]
```

---

#### **`getLevelorder()`**  

Returns a list of (key, value) pairs in level-order traversal.  

**Implementation**: Calls `levelorder()` traversal on `root` attribute, and append `(key, value)` pairs to the list.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
levelorder = tree.getLevelorder()
print(levelorder)  # Output: [(3, 'C'), (1, 'A'), (5, 'E'), (2, 'B'), (4, 'D')]
```

---

#### **`clear()`**  

Deletes all nodes from the tree.

**Implementation**: traverses the `root` attribute using `postorder()` and deletes all the nodes which don't have children. At the end, `root` attribute is changed to `None`

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
tree.clear()
print(tree.empty())  # Output: True
```

---

#### **`size()`**  

Returns the number of nodes in the tree.  

**Implementation**: calls the `size` method on `root` attribute (an instance of `TreeNode`).

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
print(tree.size())  # Output: 5
```

---

#### **`empty()`**  

Returns `True` if the tree is empty.  

**Implementation**: checks whether the `root` attribute equal to `None`.
**_Example_** of usage:  

```python
tree = TreeRoot()
print(tree.empty())  # Output: True
```

---

#### **`elementAccess(target_key)`**  

Returns the value of a key if it exists. Raises `KeyError` if the given key does not exist in the tree. 

**Implementation**: using the `find(target_key)` method to find the node and returns its value. 

`target_key`: The key to search for in the tree.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
value = tree.elementAccess(2)
print(value)  # Output: B
```

---

#### **`find(target_key)`**  

Returns the node with the specified key or None if the node does not exist.

**Implementation**: finds the node using rules of BST construction.

`target_key`: The key to search for in the tree.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
node = tree.find(4)
print(node.key, node.value)  # Output: 4 D
```

---

#### **`kthLargestElement(k)`**  
`k` (int): The position of the desired element in the sorted order of the tree's elements, where 1 corresponds to the largest element.

Returns the k-th largest element in the tree. Raises `TypeError`, if `k` is not an integer. 

**Implementation**: calls `kthLargestElement(k)` on `root` attribute.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
kth_largest = tree.kthLargestElement(2)
print(kth_largest.key)  # Output: 4
```

---

#### **`kthSmallestElement(k)`**  
`k` (int): The position of the desired element in the sorted order of the tree's elements, where 1 corresponds to the smallest element.

Returns the k-th smallest element in the tree. Raises `TypeError`, if `k` is not an integer. 

**Implementation**: calls `kthSmallestElement(k)` on `root` attribute

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
kth_smallest = tree.kthSmallestElement(3)
print(kth_smallest.key)  # Output: 3
```

---

#### **`findmin()`**  
Returns the smallest key in the tree.

**Implementation**: calls `findmin()` on `root` attribute

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
min_key = tree.findmin()
print(min_key)  # Output: 1
```

---

#### **`findmax()`**  

Returns the largest key in the tree.  

**Implementation**: calls `findmax()` on `root` attribute

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
max_key = tree.findmax()
print(max_key)  # Output: 5
```

---

#### **`previous(node, target)`**  
`node` (TreeNode): The root of a tree or subtree in which the predecessor is to be found.

`target`: The key for which the in-order predecessor is to be found.

Returns `TreeNode` which is the in-order predecessor of the `target` key, or `None` if the key is already a minimum.Raises `TypeError` if `node` is not an instance of `TreeNode` or its subclass.

**Implementation**: finds the predecessor node using rules of BST construction.

**_Example_** of usage:  

```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
predecessor = tree.previous(root, 4)
print(predecessor.key)  # Output: 3
```

---

#### **`next(node, target)`**  
`node` (TreeNode): The root of a tree or subtree in which the successor is to be found.

`target`: The key for which the in-order successor is to be found.

Returns the in-order successor of the `target` key, or `None` if the key is a maximum. Raises `TypeError` if `node` is not an instance of `TreeNode` or its subclass.

**Implementation**: finds the successor node using rules of BST construction.

**_Example_** of usage:  
```python
T = TreeNode
root = T(3, value="C", left=T(1, value="A", right=T(2, value="B")), right=T(5, value="E", left=T(4, value="D")))
tree = TreeRoot(root)
successor = tree.next(root, 2)
print(successor.key)  # Output: 3
```

---


## `AVLTreeNode` Class (from `AVLtree.py`)

The `AVLTreeNode` class extends the `TreeNode` class to include height information for balancing in an AVL Tree.

#### Attributes:
- **height**: The height of the node in the AVL tree.

### Methods:
#### **`__init__()`**: 
Constructor. Initializes an AVL tree node with a key, value, height and optional left and right children. The height defaults to `1`.. 

### `AVLtree` Class (from `AVLtree.py`)

The `AVLtree` class extends the `TreeRoot` class to provide AVL tree functionality, including insertion, deletion, merging and balancing operations.

#### Methods:
Here’s the rewritten documentation for the `AVLtree` class methods, following the same style as before. Each method includes a description, example usage, and expected output, using the **same tree structure** for consistency:

---

### **`__init__`**  
Initializes an AVL tree with an optional root node and comparator function.  

---

#### **`insert(new_key, new_value)`**  

Inserts a new key-value pair into the AVL tree.  

`new_key`: The key of the new node.

`new_value`: The value of the new node.

**Implementation**: finds the place where to insert the new node using `_insert_recursive()`, and then gradually updates the heights of nodes using `_updateHeight()` and balances the tree using `_balance()`, `_left_rotate()` and `_right_rotate()`.  

**_Example_** of usage:  

```python
avl_tree = AVLtree()
avl_tree.insert(3, "C")
avl_tree.insert(1, "A")
avl_tree.insert(2, "B")
avl_tree.insert(5, "E")
avl_tree.insert(4, "D")
print(avl_tree.getInorder())  # Output: [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]
```

---

#### **`delete(key)`**  
Deletes a node with the specified key from the AVL tree.

`key`: The key of the node to be deleted.

**Implementation**: finds the 'key' using the `_delete_recursive()`, deletes it, replaces node with its succesor, using `next()` and then gradually updates the heights of nodes using `_updateHeight()` and balances the tree, using `_balance()`, `_left_rotate()` and `_right_rotate()`.

**_Example_** of usage:  

```python
avl_tree = AVLtree()
avl_tree.insert(3, "C")
avl_tree.insert(1, "A")
avl_tree.insert(2, "B")
avl_tree.insert(5, "E")
avl_tree.insert(4, "D")
avl_tree.delete(2)
print(avl_tree.getInorder())  # Output: [(1, 'A'), (3, 'C'), (4, 'D'), (5, 'E')]
```

---

#### **`merge(tree1, tree2)`**  
Returns a new balanced AVL tree containing all key-value pairs from both input trees. The  comparator of a new tree is the same with the comparator in tree1.

`tree1` (AVLtree): The first AVL tree to be merged.

`tree2` (AVLtree): The second AVL tree to be merged.

**Implementation**: creates the new tree, where inserts all nodes from `tree1` and `tree2`, using `insert()` and `comparator` from the first tree.

**_Example_** of usage:  

```python
avl_tree1 = AVLtree()
avl_tree1.insert(3, "C")
avl_tree1.insert(1, "A")
avl_tree1.insert(2, "B")

avl_tree2 = AVLtree()
avl_tree2.insert(5, "E")
avl_tree2.insert(4, "D")

merged_tree = AVLtree().merge(avl_tree1, avl_tree2)
print(merged_tree.getInorder())  
# Output: [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]
```

---

#### **`buildTheBalancedTree(array, comparator = DEFAULT_COMPARATOR, isSorted=False )`**  

Constructs a balanced AVL tree from an array of key-value pairs.  

`array`: A list of tuples, where each tuple contains a key and its corresponding value.

`comparator` (Callable): The comparator function to use for key comparisons.

`isSorted(bool)`: Indicator, which tells whether the input is sorted according to comparator rules, is `False` by default.

**Implementation**: The array is sorted as needed using the provided comparator. It is then recursively divided in half, and the middle element of each subarray is added as a tree node.

**_Example_** of usage:  

```python
sorted_array = [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]
avl_tree = AVLtree().buildTheBalancedTree(sorted_array, lambda a, b: a - b, isSorted=True)
print(avl_tree.getInorder())  
# Output: [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')]
```

---

#### **`getHeight(node)`**  

Returns the height attribute of the given node. 


`node` (AVLTreeNode): The node whose height is to be determined.

**Implementation**: returns the `height` attribute of the `node`.

**_Example_** of usage:  
```python
avl_tree = AVLtree()
avl_tree.insert(3, "C")
avl_tree.insert(1, "A")
avl_tree.insert(2, "B")
height = avl_tree.getHeight(avl_tree.root)
print(height)  
# Output: 2
```

---

#### **`isBalanced()`**  
Checks whether the AVL tree is balanced. Returns `True` if the tree is balanced, `False` otherwise.

**Implementation**: It checks if the `abs(balance_factor)` of each node is less than `2`, where balance_factor is equal to `getHeight(left_subtree) - getHeight(right_subtree)``.

**_Example_** of usage:  

```python
avl_tree = AVLtree()
avl_tree.insert(3, "C")
avl_tree.insert(1, "A")
avl_tree.insert(2, "B")
avl_tree.insert(5, "E")
avl_tree.insert(4, "D")
print(avl_tree.isBalanced())  
# Output: True
```

---

### Helper Methods (Internal Methods)
- **`_delete_recursive`**: Helper method for recursively deleting a node.
- **`_insert_recursive`**: Helper method for recursively inserting a new key-value pair.
- **`_updateHeight`**: Updates the height of the node.
- **`_balance`**: Balances the AVL tree at the current node.
- **`_right_rotate`**: Performs a right rotation on the given node.
- **`_left_rotate`**: Performs a left rotation on the given node.
- **`_buildTheBalancedTree_helper`**: Helper method for building a balanced AVL tree from a sorted array.
- **`mergeList`**: Static method, which merges two sorted lists of key-value pairs into a single sorted list.
