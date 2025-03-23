from AVLtree import AVLtree, TreeNode
import unittest

COMPARATOR1 = lambda a, b: b - a 
COMPARATOR2 = lambda a, b: a - b

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        self.tree1 = AVLtree()
        self.tree2 = AVLtree()
        self.emptyTree = AVLtree()

    def test_insert_into_empty_tree(self):
        self.tree1.insert(10, "A")
        self.assertEqual(self.tree1.elementAccess(10), "A")
        self.assertTrue(self.tree1.isBalanced())

    def test_insert_multiple_keys(self):   
        keys = [10, 20, 30, 40, 35, 50]    #test insert left and right-left rotation
        for key in keys:
            self.tree1.insert(key, str(key))
        for key in keys:
            self.assertEqual(self.tree1.elementAccess(key), str(key))
        self.tree1.insert(10, "a")
        self.assertEqual(self.tree1.elementAccess(10), "10")      #insert key with the same weight
        self.assertTrue(self.tree1.isBalanced())
        
        keys = [8, 7, 15]                 #test insert right and left-right rotation
        for key in keys:
            self.tree1.insert(key, str(key))
        for key in keys:
            self.assertEqual(self.tree1.elementAccess(key), str(key))
        self.assertTrue(self.tree1.isBalanced())

    def test_delete(self):
        keys = [10, 20, 30, 40, 35, 50, 8, 7, 15]
        for key in keys:
            self.tree1.insert(key, str(key))
        test_cases = [(self.tree1, 15),      # delete a leaf node
                      (self.tree1, 20),      # delete a node without left child
                      (self.tree1, 8),       # delete a node without right child
                      (self.tree1, 10),      # delete a node with two childs
                      (self.tree1, 35)       # delete a root
        ]
        for tree, key_to_delete in test_cases:
            with self.subTest(tree = tree.__repr__(), node_to_delete = key_to_delete):
                tree.delete(key_to_delete)
                self.assertIsNone(tree.find(key_to_delete))
                self.assertTrue(tree.isBalanced())
        self.tree2.delete(100)             # delete from an empty tree
        self.assertIsNone(self.tree2.root)
        self.tree1.delete(100)             # delete non-existing key
        self.assertEqual(self.tree1.size(), 4) # delete non-existing key

    def test_stress_test_balancing(self):
        keys = list(range(100))
        for key in keys:
            self.tree1.insert(key, str(key))
        for key in keys:
            self.tree1.delete(key)
        self.assertIsNone(self.tree1.root)                           #when we delete all nodes the tree should be None????

    def test_merge_two_non_empty_trees(self):
        keys1 = [10, 20, 30, 40, 35, 50]
        for key in keys1:
            self.tree1.insert(key, str(key))
        keys2 = [8, 7, 15]
        for key in keys2:
            self.tree2.insert(key, str(key))
        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)
        keys = keys1 + keys2
        for key in keys:
            self.assertEqual(merged_tree.elementAccess(key), str(key))
        self.assertTrue(merged_tree.isBalanced())    
    
    def test_merge_with_an_empty_tree(self):
        keys = [10, 20, 30, 40, 35, 50]
        for key in keys:
            self.tree1.insert(key, str(key))
        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)
        for key in keys:
            self.assertEqual(merged_tree.elementAccess(key), str(key))
        self.assertEqual(merged_tree.size(), self.tree1.size())
        self.assertTrue(merged_tree.isBalanced())
        
    def test_merge_two_empty_trees(self):
        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)
        self.assertTrue(merged_tree.empty())

    def test_merge_trees_with_overlapping_keys(self): 
        self.tree1.insert(5, "A")
        self.tree1.insert(3, "B")
        self.tree2.insert(5, "C")
        self.tree2.insert(8, "D")

        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)

        self.assertEqual(merged_tree.elementAccess(5), "A")  # Value from tree1 takes precedence
        self.assertEqual(merged_tree.elementAccess(3), "B")
        self.assertEqual(merged_tree.elementAccess(8), "D")

        self.assertTrue(merged_tree.isBalanced())

    def test_merge_trees_with_different_comparators(self):
        self.tree1.comparator = COMPARATOR1
        self.tree2.comparator = COMPARATOR2
        
        self.tree1.insert(5, "A")
        self.tree1.insert(3, "B")
        self.tree2.insert(5, "C")
        self.tree2.insert(8, "D")
        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)
        
        self.assertEqual(self.tree1.comparator, COMPARATOR1)

        self.assertEqual(merged_tree.getInorder(), [(8, "D"), (5, "A"), (3, "B")])

        self.assertTrue(merged_tree.isBalanced())

    def test_merge_stress_test(self):
        for i in range(100):
            self.tree1.insert(i, i)
        for i in range(50, 150):
            self.tree2.insert(i, i + 1000)

        merged_tree = self.emptyTree.merge(self.tree1, self.tree2)

        for i in range(100):
            self.assertEqual(merged_tree.elementAccess(i), i)
        for i in range(100, 150):
            self.assertEqual(merged_tree.elementAccess(i), i + 1000)

        self.assertTrue(merged_tree.isBalanced())

    def test_buildTheSingleNodeBalancedTree(self):
        tree = AVLtree().buildTheBalancedTree([(1, "A")])                     #single node tree
        self.assertEqual(tree.elementAccess(1), "A")
        self.assertEqual(tree.size(), 1)
    
    def test_buildTreefromSortedList(self):
        array = [(1, "A"), (2, "B"), (3, "C"), (4, "D"), (5, "E")]
        tree = AVLtree().buildTheBalancedTree(array, isSorted=True)
        for (key, value) in array:
            self.assertEqual(tree.elementAccess(key), value)
        self.assertTrue(tree.isBalanced())
        self.assertEqual(tree.size(), 5)
        self.assertEqual(tree.getInorder(), array)

    def test_unsorted_array(self):
        array = [(5, "E"), (2, "B"), (1, "A"), (4, "D"), (3, "C")]
        tree = AVLtree().buildTheBalancedTree(array, comparator=COMPARATOR1)
        for (key, value) in array:
            self.assertEqual(tree.elementAccess(key), value)
        self.assertTrue(tree.isBalanced())
        self.assertEqual(tree.size(), 5)
        self.assertEqual(tree.getInorder(), [(5, "E"), (4, "D"), (3, "C"), (2, "B"), (1, "A")])

    def test_large_array(self):
        array = [(i, chr(i)) for i in range(100)]
        tree = AVLtree().buildTheBalancedTree(array)
        for (key, value) in array:
            self.assertEqual(tree.elementAccess(key), value)
        self.assertTrue(tree.isBalanced())
        self.assertEqual(tree.size(), 100)
        self.assertEqual(tree.getInorder(), array)
            

if __name__ == '__main__':
    unittest.main(verbosity=2)