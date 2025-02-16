Idea and basic description of the problem.
	
Search trees are foundational data structures that organize data in sorted order while 
maintaining efficient insertion, deletion, and lookup operations. These trees include 
binary (e.g., AVL, red-black, treap, splay) and non-binary (e. g. 2-3 tree). The project 
aims to implement these types of trees and create Python library that provides a unified interface 
for operations on these tree types, including:
	
-	Support for methods like PreOrder, InOrder, PostOrder, LevelOrder, Insert, Delete, Find, ElementAccess, Merge, Size, 
	Empty, Ñlear, FindMin, FindMax, Previous, Next, KthElement and GetMetaValue.

-	Additionally, the library will support storing auxiliary data in nodes, with user-defined rules for calculation (e.g., sums). 
	Users can configure key comparison operation, which is used during building the tree.

Form and description of inputs and outputs.

Input: A series of tree operations
-	Constructor(comparator, AuxiliaryFunction)
-	PreOrder()
-	InOrder()
-	PostOrder()
-	LevelOrder()
-	Merge(tree)
-	Size()
-	Empty()
-	Clear()
-	Insert(key, value)
-	Delete(key)
-	Find(key) 
-	ElementAccess(key)
-	FindMin()
-	FindMax()
-	Previous(key)
-	Next(key)
-	KthElement(k)
-	GetMetaValue(key) 

Outputs: Results of query operations:
-	PreOrder(), InOrder(), PostOrder(), LevelOrder() returns the list of elements in corresponding order.
-	Size() returns the number of nodes in the tree.
-	Empty() returns True if the Size() equal zero.
-	ElementAccess(key) returns value of the key if exists.
-	Find(key) returns the node with the specified key or it returns None if node does not exist.
-	FindMin() and FindMax() return the smallest and largest keys, respectively.
-	Previous(key) returns the in-order predecessor of a given node
-	Next(key) returns the successor of the key in sorted order.
-	KthElement(k) returns k-th biggest element of the tree.
-	GetMetaValue(key) returns the auxiliary value in the corresponding key.
