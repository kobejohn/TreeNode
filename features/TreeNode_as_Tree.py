# Feature:  TreeNode as Node
# Actors:   TreeNode (TN)

import unittest as ut

from simpletree import simpletree as st
#import _specification_data as spec_data

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Responsibilities Key Examples
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class TN_access_to_parent(ut.TestCase):
    def test_TN__parent_is_none_by_default(self):
        node = st.TreeNode()
        self.assertIsNone(node.parent)

    def test_TN__parent_is_a_node_when_it_exists(self):
        parent = st.TreeNode(a="parent")
        child = st.TreeNode(a="child")
        parent.graft_child(child)
        self.assertIsInstance(child.parent, st.TreeNode)

    def test_TN_does_not_provide_set_or_del_access_to_parent(self):
        node = st.TreeNode()
        self.assertRaises(AttributeError, setattr, node, "parent", 1)
        self.assertRaises(AttributeError, delattr, node, "parent")


class TN_access_to_children(ut.TestCase):
    def test_TN__graft_child_handles_linking_of_new_child_node(self):
        self.assertEqual(id(self.child1.parent), id(self.parent))
        child_ids_spec = [id(self.child1), id(self.child2)]
        child_ids = [id(child) for child in self.parent.children]
        self.assertItemsEqual(child_ids, child_ids_spec)

    def test_TN_children_property_provides_sequence_of_children(self):
        for child in self.parent.children:
            self.assertIn(child.a, ["child1", "child2"])

    def test_TN_children_property_does_not_provide_set_del_access_to_children(self):
        self.assertRaises(AttributeError, setattr, self.parent, "children", 1)
        self.assertRaises(AttributeError, delattr, self.parent, "children")

    def test_TN_children_property_does_not_allow_append_etc_access_to_children(self):
        self.assertRaises(AttributeError, getattr, self.parent.children, "append")

    def setUp(self):
        self.parent = st.TreeNode(a="parent")
        self.child1 = st.TreeNode(a="child1")
        self.child2 = st.TreeNode(a="child2")
        self.parent.graft_child(self.child1)
        self.parent.graft_child(self.child2)


class In_Order_Access_to_Nodes(ut.TestCase):
    def test__in_order_nodes__provides_sequence_with_only_self_when_only_one_self_in_tree(self):
        node_string_list_spec = ["root"]
        node_string_list = [node.name for node in self.root.in_order_nodes]
        self.assertEqual(node_string_list_spec, node_string_list)

    def test__in_order_nodes__provides_in_order_sequence_for_full_tree(self):
        self.root.graft_child(self.a)
        self.root.graft_child(self.b)
        self.b.graft_child(self.c)
        node_string_list_spec = ["root","a","b","c"]
        node_string_list = [node.name for node in self.root.in_order_nodes]
        self.assertEqual(node_string_list_spec, node_string_list)

    def test__in_order_nodes__provides_in_order_sequence_limited_to_subtree(self):
        self.root.graft_child(self.a)
        self.root.graft_child(self.b)
        self.b.graft_child(self.c)
        node_string_list_spec = ["b","c"]
        node_string_list = [node.name for node in self.b.in_order_nodes]
        self.assertEqual(node_string_list_spec, node_string_list)

    def setUp(self):
        self.root = st.TreeNode(name = "root")
        self.a = st.TreeNode(name = "a")
        self.b = st.TreeNode(name = "b")
        self.c = st.TreeNode(name = "c")


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Internal Key Examples
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class TN_should_not_allow_cycles(ut.TestCase):
    def test_TN__graft_child_removes_child_from_previous_parent(self):
        parent1 = st.TreeNode()
        parent2 = st.TreeNode()
        child = st.TreeNode()
        parent1.graft_child(child)
        parent2.graft_child(child)
        self.assertEqual([], list(parent1.children))

        #todo: ... that's probably not enough but for now that's it


class TN__trim_removes_double_link_between_parent_and_child(ut.TestCase):
    def test_TN__trim_removes_child_from_parent_and_sets_child_parent_to_None(self):
        parent = st.TreeNode()
        child = st.TreeNode()
        parent.graft_child(child)
        child.trim()
        self.assertEqual(None, child.parent)
        self.assertEqual([], list(parent.children))



if __name__ == '__main__':
    ut.main()
