import unittest
from binarySearchTree import TreeNode, TreeRoot 

class TestTreeNode(unittest.TestCase):

    def setUp(self):
        T = TreeNode
        self.empty_tree = TreeRoot()
        self.single_node = TreeRoot(root = T(1, value="A"))
        self.tree = TreeRoot(root =T(5, "A", T(3, "B", T(1, "C"), T(4, "D")), T(8, "E", None, T(9, "F"))))

    def test_pre_order(self):
        self.assertEqual(self.empty_tree.getPreorder(), [])
        self.assertEqual(self.single_node.getPreorder(), [(1, "A")])
        self.assertEqual(self.tree.getPreorder(), [(5, "A"), (3, "B"), (1, "C"), (4, "D"), (8, "E"), (9, "F")])
   
    def test_in_order(self):
        self.assertEqual(self.empty_tree.getInorder(), [])
        self.assertEqual(self.single_node.getInorder(), [(1, "A")])
        self.assertEqual(self.tree.getInorder(), [(1, "C"), (3, "B"), (4, "D"), (5, "A"), (8, "E"), (9, "F")])

    def test_reverse_order(self):
        self.assertEqual(self.empty_tree.getReverseorder(), [])
        self.assertEqual(self.single_node.getReverseorder(), [(1, "A")])
        self.assertEqual(self.tree.getReverseorder(), [(9, "F"), (8, "E"), (5, "A"), (4, "D"), (3, "B"), (1, "C")])

    def test_post_order(self):
        self.assertEqual(self.empty_tree.getPostorder(), [])
        self.assertEqual(self.single_node.getPostorder(), [(1, "A")])
        self.assertEqual(self.tree.getPostorder(), [(1, "C"), (4, "D"), (3, "B"), (9, "F"), (8, "E"), (5, "A")])

    def test_level_order(self):
        self.assertEqual(self.empty_tree.getLevelorder(), [])
        self.assertEqual(self.single_node.getLevelorder(), [(1, "A")])
        self.assertEqual(self.tree.getLevelorder(), [(5, "A"), (3, "B"), (8, "E"), (1, "C"), (4, "D"), (9, "F")])
    
    def test_find_existing_key(self):
        self.assertEqual(self.single_node.find(1), TreeNode(1))
        self.assertEqual(self.tree.find(3), TreeNode(3, "A", TreeNode(1), TreeNode(4))) 

    def test_find_non_existing_key(self):
        self.assertIsNone(self.empty_tree.find(10))
        self.assertIsNone(self.single_node.find(10))
        self.assertIsNone(self.tree.find(10))

    def test_find_min(self):
        self.assertIsNone(self.empty_tree.findmin())
        self.assertEqual(self.single_node.findmin(), 1)
        self.assertEqual(self.tree.findmin(), 1)

    def test_find_max(self):
        self.assertIsNone(self.empty_tree.findmax())
        self.assertEqual(self.single_node.findmax(), 1)
        self.assertEqual(self.tree.findmax(), 9)

    def test_size(self):
        self.assertEqual(self.empty_tree.size(), 0)
        self.assertEqual(self.single_node.size(), 1)
        self.assertEqual(self.tree.size(), 6)

    def test_empty(self):
        self.assertTrue(self.empty_tree.empty())
        self.assertFalse(self.single_node.empty())
        self.assertFalse(self.tree.empty())
   
    def test_clear(self):
        self.tree.clear()
        self.assertTrue(self.tree.empty())
        self.single_node.clear()
        self.assertTrue(self.single_node.empty())
        self.empty_tree.clear()
        self.assertTrue(self.empty_tree.empty())
        
    def test_previous(self):
        self.assertIsNone(self.single_node.previous(self.single_node.root, 1))
        self.assertEqual(self.tree.previous(self.tree.root,  4), TreeNode(3, "A", TreeNode(1), TreeNode(4)))  
        self.assertEqual(self.tree.previous(self.tree.root, 10), TreeNode(9))                        #the key 10 is not in the tree
 
    def test_next(self):
        self.assertIsNone(self.single_node.next(self.single_node.root, 1))
        self.assertEqual(self.tree.next(self.tree.root, 4), self.tree.root)  
        self.assertEqual(self.tree.next(self.tree.root, 0), TreeNode(1))                             #the key 0 is not in the tree

    def test_kth_element(self):
        self.assertIsNone(self.empty_tree.kthLargestElement(10))
        self.assertEqual(self.single_node.kthLargestElement(1), self.single_node.root)
        self.assertEqual(self.tree.kthLargestElement(3), self.tree.root)
        
    def test_kth_smallest_element(self):
        self.assertIsNone(self.empty_tree.kthSmallestElement(10))
        self.assertEqual(self.single_node.kthSmallestElement(1), self.single_node.root)
        self.assertEqual(self.tree.kthSmallestElement(3), TreeNode(4))

    def test_element_access(self):
        self.assertEqual(self.single_node.elementAccess(1), "A")      
        self.assertEqual(self.tree.elementAccess(3), "B")
        self.assertEqual(self.tree.elementAccess(1), "C")#the key is a list
    
    def test_errors(self):
        with self.assertRaises(KeyError):  
            self.empty_tree.elementAccess(10)       
            self.single_node.elementAccess(10)
        invalid_object = "not a TreeRoot"
        with self.assertRaises(TypeError):
            self.tree == invalid_object
            self.tree.kthLargestElement("a")
            self.tree.kthSmallestElement("b")
            self.tree.next(invalid_object, 5)
            self.tree.previous(invalid_object, 5)
        
    def test_getMetaValue(self):
        self.assertIsNone(self.empty_tree.getMetaValue(10, f))
        self.assertEqual(self.single_node.getMetaValue(1, f), "AXX")
        self.assertIsNone(self.single_node.getMetaValue(15, f))
        self.assertEqual(self.tree.getMetaValue(5, f), "ABCXXDXXEXFXX")
        self.assertEqual(self.tree.getMetaValue(3, f), "BCXXDXX")

    def test_iter(self):
        self.assertEqual([(key, value) for key, value in self.empty_tree], [])
        self.assertEqual([(key, value) for key, value in self.single_node], [(1, "A")])
        self.assertEqual([(key, value) for key, value in self.tree], [(1, 'C'), (3, 'B'), (4, 'D'), (5, 'A'), (8, 'E'), (9, 'F')])

    def test_eq(self):
        T = TreeNode
        tree1 = TreeRoot(root =T(5, "A", T(3, "B", T(1, "C"), T(4, "D")), T(8, "E", None, T(9, "F"))))
        empty_tree = TreeRoot()
        tree2 = TreeRoot(T(2))
        self.assertEqual(tree1, self.tree)
        self.assertNotEqual(tree1, self.single_node)
        self.assertNotEqual(tree1, self.empty_tree)
        self.assertEqual(self.empty_tree, empty_tree)
        self.assertNotEqual(self.single_node, tree2)


def f(left_subtree = None, right_subtree = None, node_value = None):
    return (node_value or 'X') + (left_subtree or 'X') + (right_subtree or 'X')

if __name__ == '__main__':
    unittest.main(verbosity=2)