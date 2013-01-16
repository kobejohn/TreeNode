# -*- coding: utf-8 -*-
"""
treenode
~~~~~~~~~~

Doubly-linked tree structure with arbitrary data attributes.

:copyright: (c) 2012 by John Nieri.
:license: MIT, see LICENSE for more details.
"""
from collections import deque


class TreeNode(object):
    """Single object that provides both node and tree behavior.

    Note on equality:
    Equality is based on the values for all data attributes.

    Note on subclassing:
    The intention is to subclass TreeNode and override __init__ to provide
    a standard set of attributes for a particular application.
    """
    def __init__(self, **attributes):
        """Create a treenode with specified attributes.

        Arguments:
        keys: use valid python names as they will be used to create attributes

        """
        self._parent = None
        self._children = dict() #identify children without depending on equality
        self._data_attributes = [] #list of the data attributes of this node
        existing_class_attributes = dir(self)
        for name, value in attributes.items():
            #disallow names that exist in the class
            if name in existing_class_attributes:
                raise ValueError('Requested attribute name, {}, already exists in the object.'.format(name))
            #store the new attribute and value
            setattr(self, name, value)
            self._data_attributes.append(name)

    def __ne__(self, other):
        """Compare the nodes based on equality of their custom attributes."""
        #first eliminate objects that don't have the custom attributes
        try:
            #use sets since the attributes may not be stored in the same order
            self_set = set(self._data_attributes)
            other_set = set(other._data_attributes)
        except AttributeError:
            return True
        #next eliminate objects that have different custom attribute names
        if self_set != other_set:
            return True
        #next eliminate objects that have any different data values
        return any(getattr(self, attr) != getattr(other, attr)
                   for attr in self._data_attributes)

    def __eq__(self, other):
        return not (self != other)

    def __unicode__(self):
        line_list = ['TreeNode:',
                     '    parent: {}'.format('none' if self.parent is None else 'yes'),
                     '    children: {}'.format(len(list(self.children)))]
        for attr_name in self._data_attributes:
            line_list.append('    {}: {}'.format(attr_name, getattr(self,attr_name)))
        return '\n'.join(line_list)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return unicode(self)

    def trim(self):
        """Remove double link between self and parent.

        Note: This is the primary method for disconnecting nodes.

        """
        #remove link *from* parent
        try:
            del self.parent._children[id(self)]
        except AttributeError:
            pass #didn't have a parent
            #remove link *to* parent
        self._parent = None

    def graft_child(self, child):
        """Doubly link self with child AND remove double link to current parent.

        Note: This is the primary method for connecting nodes.

        """
        #remove double link with child's parent
        child.trim()
        #create double link with child
        child._parent = self
        self._children[id(child)] = child

    @property #get-only to avoid mistakes with double-linking
    def parent(self):
        """Get the parent. """
        return self._parent

    @property #get-only to avoid mistakes with double-linking
    def children(self):
        """Get a list of children."""
        return self._children.values()

    @property
    def in_order_nodes(self):
        """In-order generate all nodes in the (sub)tree with self as root."""
        stack = deque()
        stack.append(self)
        while stack:
            #get the current (in-order) node
            node = stack.pop()
            #push all its children
            #reverse order makes it more natural for humans
            for child in reversed(node.children):
                stack.append(child)
            #yield the current node before any of its children
            yield node

    @property
    def post_order_nodes(self):
        """Post-order generate all nodes in the (sub)tree with self as root."""
        for node in reversed(list(self.in_order_nodes)):
            yield node #fake generator for consistency with in order nodes

    @property
    def leaves(self):
        """Generate all leaves in the (sub)tree with self as root."""
        for node in self.in_order_nodes:
            if node.is_leaf:
                yield node

    @property
    def is_leaf(self):
        """Return True if self is a leaf node. False otherwise."""
        return not self.children #i.e. no children ==> leaf
