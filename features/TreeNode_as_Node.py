# Feature:  TreeNode as Node
# Actors:   TreeNode (TN)

import unittest as ut

#from simpletree import simpletree as st
import simpletree.simpletree as st
#import _specification_data as spec_data

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Responsibilities Key Examples
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class TN_access_to_data(ut.TestCase):
    def test_TN_is_created_with_arbitrary_data_attributes_abc_and_values_123(self):
        self.assertIsInstance(self.node, st.TreeNode)

    def test_TN_provides_public_access_to_creation_attributes(self):
        self.assertEqual(self.node.a, 1)
        self.assertEqual(self.node.b, 2)
        self.assertEqual(self.node.c, 3)

#    def test_TN_provides_sequence_of_name_value_tuple_access_to_attributes(self):
#        names_values = list(self.node)
#        self.assertItemsEqual(names_values, [("a",1),("b",2),("c",3)])

    def setUp(self):
        self.node = st.TreeNode(a=1, b=2, c=3)


class TN_equality(ut.TestCase):
    def test_TN_equality_is_based_on_equality_of_all_attributes(self):
        node1 = st.TreeNode(a=1, b=2, c=3)
        node2 = st.TreeNode(a=1, b=2, c=3)
        node3 = st.TreeNode(a=1, b=2, c=30)
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)

    def test_TN_equality_is_independent_of_attribute_order(self):
        node1 = st.TreeNode(a=1, b=2, c=3)
        node2 = st.TreeNode(b=2, c=3, a=1)
        self.assertEqual(node1, node2)

    def test_TN_equality_is_false_for_nodes_with_sub_or_supersets_of_attributes(self):
        node1 = st.TreeNode(a=1, b=2, c=3)
        node2 = st.TreeNode(a=1, b=2)
        self.assertNotEqual(node1, node2)


class TN_should_be_human_readable(ut.TestCase):
    def test_TN_string_representation_displays_all_data_items_and_relatives_summary(self):
        parent = st.TreeNode()
        main = st.TreeNode(a=1, b=2)
        child1 = st.TreeNode()
        child2 = st.TreeNode()
        parent.graft_child(main)
        main.graft_child(child1)
        main.graft_child(child2)
        string_spec = "tree node:\n"\
                      "parent:   yes\n"\
                      "children: 2\n"\
                      "a:\n1\n"\
                      "b:\n2"
        self.assertEqual(string_spec, str(main))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Internal Key Examples
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class TN_keeps_list_of_user_provided_public_attributes(ut.TestCase):
    def test_TN_keeps_list_of_abc_when_created(self):
        attribute_names_spec = {"a":1, "b":2, "c":3}
        node = st.TreeNode(**attribute_names_spec)
        self.assertItemsEqual(node._custom_attributes, list(attribute_names_spec.keys()))




if __name__ == '__main__':
    ut.main()
