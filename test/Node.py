import unittest as ut

from simpletree import TreeNode

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# Public behavior
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class Nodes_Have_Data_Attributes(ut.TestCase):
    def setUp(self):
        self.values_by_name = {'a': 1, 'b': 2, 'c': 3}

    def test_create_node_with_attributes_abc(self):
        node = TreeNode(**self.values_by_name)
        for name in self.values_by_name.keys():
            self.assertTrue(hasattr(node, name), 'Should have attribute, {}, but does not.'.format(name))

    def test_create_node_with_values_123(self):
        node = TreeNode(**self.values_by_name)
        for name, value in self.values_by_name.items():
            self.assertEqual(getattr(node, name), value)

    def test_creating_a_node_with_an_existing_class_attribute_name_raises_ValueError(self):
        self.assertRaises(ValueError, TreeNode, __doc__ = 1)


class Nodes_Are_Equal_Only_If_Data_Items_Equal(ut.TestCase):
    def test_nodes_with_same_attributes_and_values_are_equal(self):
        attributes = {'a': 1, 'b': 2}
        node_1 = TreeNode(**attributes)
        node_2 = TreeNode(**attributes)
        self.assertEqual(node_1, node_2)

    def test_node_equality_is_independent_of_original_attribute_order(self):
        node_1 = TreeNode(a= 1, b= 2)
        node_2 = TreeNode(b= 2, a= 1)
        self.assertEqual(node_1, node_2)

    def test_nodes_with_different_attributes_are_not_equal(self):
        node_1 = TreeNode(a= 1, b= 2)
        node_2 = TreeNode(a= 1)
        self.assertNotEqual(node_1, node_2)

    def test_nodes_with_same_attributes_but_different_value_are_not_equal(self):
        node_1 = TreeNode(a= 1, b= 2)
        node_2 = TreeNode(a= 1, b= 33)
        self.assertNotEqual(node_1, node_2)


class Nodes_Are_Human_Readable(ut.TestCase):
    def test_TN_string_representation_displays_all_data_items_and_relatives_summary(self):
        parent = TreeNode()
        main = TreeNode(a=1, b=2)
        parent.graft_child(main)
        main.graft_child(TreeNode())
        main.graft_child(TreeNode())
        string_spec = 'TreeNode:\n'\
                      '    parent:   yes\n'\
                      '    children: 2\n'\
                      '    a: 1\n'\
                      '    b: 2'
        self.assertEqual(str(main), string_spec)


if __name__ == '__main__':
    ut.main()
