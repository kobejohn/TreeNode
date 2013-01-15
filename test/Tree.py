import unittest as ut

from simpletree import TreeNode

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Public behavior
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class A_Node_Has_A_Parent(ut.TestCase):
    def test_parent_is_none_by_default(self):
        node = TreeNode()
        self.assertIsNone(node.parent)

    def test_parent_is_an_attribute(self):
        node = TreeNode()
        self.assertTrue(hasattr(node, 'parent'))

    def test_parent_raises_AttributeError_when_set_directly(self):
        node = TreeNode()
        self.assertRaises(AttributeError, setattr, node, 'parent', 1)


class A_Node_Has_Children(ut.TestCase):
    def test_children_is_an_empty_sequence_by_default(self):
        node = TreeNode()
        self.assertItemsEqual(node.children, tuple())

    def test_children_is_an_attribute(self):
        node = TreeNode()
        self.assertTrue(hasattr(node, 'children'))

    def test_children_is_a_sequence(self):
        node = TreeNode()
        node.graft_child(TreeNode())
        self.assertTrue(node.children) #True, e.g. not empty list

    def test_children_raise_AttributeError_when_set_directly(self):
        node = TreeNode()
        self.assertRaises(AttributeError, setattr, node, 'children', tuple())


class Connecting_and_Disconnecting_Nodes(ut.TestCase):
    def test_graft_doubly_links_parent_and_child(self):
        parent = TreeNode(name = 'parent')
        child = TreeNode(name = 'child')
        parent.graft_child(child)
        #assert children of parent are correct
        child_ids_of_parent = [id(c) for c in parent.children]
        child_ids_of_parent_spec = [id(child)]
        self.assertItemsEqual(child_ids_of_parent, child_ids_of_parent_spec)
        #assert parent of children is correct
        self.assertEqual(id(child.parent), id(parent))

    def test_trim_removes_double_link_between_parent_and_child_to_avoid_cycles(self):
        parent = TreeNode(name = 'parent')
        child = TreeNode(name = 'child')
        parent.graft_child(child)
        child.trim()
        #assert child no longer in children of parent
        child_ids_of_parent = [id(c) for c in parent.children]
        child_ids_of_parent_spec = list()
        self.assertItemsEqual(child_ids_of_parent, child_ids_of_parent_spec)
        #assert parent is None for the child
        self.assertIsNone(child.parent)

    def test_trim_on_a_node_with_no_parent_does_nothing(self):
        node = TreeNode()
        node.trim()
        self.assertIsNone(node.parent) #still None


class A_Node_Has_Leaves(ut.TestCase):
    def test_node_self_identifies_as_leaf_if_no_children(self):
        node = TreeNode()
        self.assertTrue(node.is_leaf)

    def test_node_self_identifies_as_not_leaf_if_any_children(self):
        node = TreeNode()
        node.graft_child(TreeNode())
        self.assertFalse(node.is_leaf)

    def test_single_node_has_itself_as_only_leaf(self):
        root = TreeNode()
        leaf_ids = [id(leaf) for leaf in root.leaves]
        leaf_ids_spec = [id(root)]
        self.assertEqual(leaf_ids, leaf_ids_spec)

    def test_simple_binary_tree_with_three_levels_has_4_leaves(self):
        #first level
        a0 = TreeNode(name='a0')
        #second level
        b0 = TreeNode(name='b0')
        b1 = TreeNode(name='b1')
        #third level
        c0 = TreeNode(name='c0')
        c1 = TreeNode(name='c1')
        c2 = TreeNode(name='c2')
        c3 = TreeNode(name='c3')
        #attach everything
        a0.graft_child(b0)
        a0.graft_child(b1)
        b0.graft_child(c0)
        b0.graft_child(c1)
        b1.graft_child(c2)
        b1.graft_child(c3)
        #confirm leaves
        leaf_names = [leaf.name for leaf in a0.leaves]
        leaf_names_spec = ['c0','c1','c2','c3']
        self.assertItemsEqual(leaf_names, leaf_names_spec)


class Traversing_A_Tree(ut.TestCase):
    def setUp(self):
        self.root = TreeNode(name = 'root')
        self.a = TreeNode(name = 'a')
        self.b = TreeNode(name = 'b')
        self.c = TreeNode(name = 'c')

    def test_node_generates_in_order_traversal_from_self(self):
        self.root.graft_child(self.a)
        self.root.graft_child(self.b)
        self.b.graft_child(self.c)
        names = [node.name for node in self.root.in_order_nodes]
        names_spec = ['root', 'a', 'b', 'c']
        self.assertSequenceEqual(names, names_spec)

    def test_node_generates_post_order_traversal_from_self(self):
        self.root.graft_child(self.a)
        self.root.graft_child(self.b)
        self.b.graft_child(self.c)
        names = [node.name for node in self.root.post_order_nodes]
        names_spec = ['c', 'b', 'a', 'root']
        self.assertSequenceEqual(names, names_spec)

    def test_node_generates_only_self_when_no_parent_or_children(self):
        node_string_list_spec = ['root']
        node_string_list = [node.name for node in self.root.in_order_nodes]
        self.assertEqual(node_string_list_spec, node_string_list)

    def test_node_generates_only_nodes_including_and_below_self_in_tree(self):
        self.root.graft_child(self.a)
        self.root.graft_child(self.b)
        self.b.graft_child(self.c)
        names = [node.name for node in self.b.in_order_nodes]
        names_spec = ['b', 'c'] #i.e. 'a' is not in there
        self.assertSequenceEqual(names, names_spec)


if __name__ == '__main__':
    ut.main()
