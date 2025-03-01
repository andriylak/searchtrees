import unittest
from binarySearchTree import TreeNode 

comparator = lambda a, b: abs(a) - abs(b)

def f(left_subtree = None, right_subtree = None, node_value = None):
    """
    auxiliary data function
    """
    return (right_subtree or '') + (node_value or '') + (left_subtree or '') 

class TestComparator(unittest.TestCase):
    def setUp(self):
        T = TreeNode
        self.empty_tree = T(comparator=comparator)
        self.single_node = T(-1, value="A", comparator=comparator)
        self.tree = T(-5, "A", comparator=comparator,
                  left=T(-3, "B", T(-1, "C"), T(-4, "D")), 
                  right=T(-8, "E", None, T(-9, "F")))

    def test_pre_order(self):
        self.assertEqual(self.empty_tree.preorder(), [])
        self.assertEqual(self.single_node.preorder(), [(-1, "A")])
        self.assertEqual(self.tree.preorder(), [(-5, "A"), (-3, "B"), (-1, "C"), (-4, "D"), (-8, "E"), (-9, "F")])

    def test_in_order(self):
        self.assertEqual(self.empty_tree.inorder(), [])
        self.assertEqual(self.single_node.inorder(), [(-1, "A")])
        self.assertEqual(self.tree.inorder(), [(-1, "C"), (-3, "B"), (-4, "D"), (-5, "A"), (-8, "E"), (-9, "F")])

    def test_post_order(self):
        self.assertEqual(self.empty_tree.postorder(), [])
        self.assertEqual(self.single_node.postorder(), [(-1, "A")])
        self.assertEqual(self.tree.postorder(), [(-1, "C"), (-4, "D"), (-3, "B"), (-9, "F"), (-8, "E"), (-5, "A")])

    def test_level_order(self):
        self.assertEqual(self.empty_tree.levelorder(), [])
        self.assertEqual(self.single_node.levelorder(), [(-1, "A")])
        self.assertEqual(self.tree.levelorder(), [(-5, "A"), (-3, "B"), (-8, "E"), (-1, "C"), (-4, "D"), (-9, "F")])

    def test_find_existing_key(self):
        func = lambda a, b: abs(a) - abs(b)
        self.assertEqual(self.single_node.find(-1), TreeNode(-1, "A", comparator = comparator))
        self.assertEqual(self.tree.find(-1), TreeNode(-1, "C", comparator = comparator))

    def test_find_non_existing_key(self):
        self.assertIsNone(self.empty_tree.find(10))
        self.assertIsNone(self.single_node.find(10))
        self.assertIsNone(self.single_node.find(1))       #in this tree there are the key with the same weight
        self.assertIsNone(self.tree.find(10))
        self.assertIsNone(self.tree.find(3))                   #in this tree there are the key with the same weight

    def test_find_min(self):
        self.assertIsNone(self.empty_tree.findmin())
        self.assertEqual(self.single_node.findmin(), -1)
        self.assertEqual(self.tree.findmin(), -1)  # The smallest key is -1 (absolute value is considered)

    def test_find_max(self):
        self.assertIsNone(self.empty_tree.findmax())
        self.assertEqual(self.single_node.findmax(), -1)
        self.assertEqual(self.tree.findmax(), -9)  # The largest key is -9 (absolute value is considered)

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

    def test_previous(self):                                          #?????
        self.assertIsNone(self.empty_tree.previous(10))
        self.assertIsNone(self.single_node.previous(-1))
        self.assertEqual(self.tree.previous(-4), TreeNode(-3, "B", TreeNode(-1, "C"), TreeNode(-4, "D"), comparator = comparator))
        self.assertEqual(self.tree.previous(10), TreeNode(-9, "F", comparator = comparator))  # Key 10 is not in the tree ????

    def test_next(self):
        self.assertIsNone(self.empty_tree.next(10))
        self.assertIsNone(self.single_node.next(-1))
        self.assertEqual(self.tree.next(-4), self.tree)
        self.assertEqual(self.tree.next(0), TreeNode(-1, "C", comparator = comparator))  # Key 0 is not in the tree

    def test_kth_element(self): 
        self.assertIsNone(self.empty_tree.kthLargestElement(10))
        self.assertEqual(self.single_node.kthLargestElement(1), TreeNode(-1, "A", comparator = comparator))
        self.assertEqual(self.tree.kthLargestElement(3), self.tree)  # 3rd largest element

    def test_element_access(self):
        self.assertIsNone(self.empty_tree.elementAccess(10))
        self.assertEqual(self.single_node.elementAccess(-1), "A")
        self.assertIsNone(self.single_node.elementAccess(10))  # Key is not in the tree
        self.assertEqual(self.tree.elementAccess(-3), "B")
        self.assertEqual(self.tree.elementAccess(-1), "C")  # Key is a leaf node

    def test_getMetaValue(self):
        self.assertIsNone(self.empty_tree.getMetaValue(10, f))
        self.assertEqual(self.single_node.getMetaValue(-1, f), "A")
        self.assertIsNone(self.single_node.getMetaValue(15, f))
        self.assertEqual(self.tree.getMetaValue(-5, f), "FEADBC")
        self.assertEqual(self.tree.getMetaValue(-3, f), "DBC")


if __name__ == "__main__":
    unittest.main(verbosity=2)
