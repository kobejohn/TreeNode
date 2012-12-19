from collections import deque

class TreeNode(object):
    def __init__(self, **kwargs):
        """Assign appropriate attributes to the node. e.g. state, action."""
        self._parent = None
        self._children = {}
        self._custom_attributes = []
        for name, value in kwargs.items():
            setattr(self, name, value)
            #store the attribute names for future use
            self._custom_attributes.append(name)
    def __eq__(self, other):
        """Compare the nodes based on their custom public data attributes."""
        #first make sure they have the same attributes
        #names can't be repeated, so set is acceptable
        try:
            self_set = set(self._custom_attributes)
            other_set = set(other._custom_attributes)
        except AttributeError:
            return False #if other doesn't even have custom attributes
        try:
            assert self_set == other_set
        except AssertionError:
            return False
            #next compare value of each attribute
        return all(getattr(self,attr)==getattr(other,attr)
            for attr in self._custom_attributes)
    def __iter__(self):
        """Make the instance generate its data items."""
        for attr_name in self._custom_attributes:
            yield (attr_name, getattr(self, attr_name))
    def __str__(self):
        final_line_list = ["tree node:",
                           "parent:   {}".format("yes" if self.parent else "none"),
                           "children: {}".format(len(list(self.children)))]
        for attr_name in self._custom_attributes:
            final_line_list.append("{}:\n{}".format(attr_name, getattr(self,attr_name)))
        return "\n".join(final_line_list)
    def __repr__(self):
        return self.__str__()

    @property
    def parent(self):
        """Provide read only access to parent."""
        return self._parent

    @property
    def children(self):
        """Generate children. Don't provide direct list access."""
        for child in self._children.values(): yield child

    @property
    def in_order_nodes(self):
        """In-order generate all nodes in tree with self as root."""
        stack = deque()
        stack.append(self)
        while stack:
            #get the current (in-order) node
            node = stack.pop()
            #add all its children to be processed (only one will be done next)
            #reverse order makes it more natural for humans just
            for child in reversed(list(node.children)):
                stack.append(child)
            yield node

    @property
    def leaves(self):
        """Generate all leaves in the tree with self as root."""
        for node in self.in_order_nodes:
            if not list(node.children): #i.e. no children ==> leaf
                yield node

    def trim(self):
        """Remove double link between self and parent."""
        #remove link from parent
        try:
            del self.parent._children[id(self)]
        except AttributeError:
            pass #didn't have a parent
        #remove link to parent
        self._parent = None


    def graft_child(self, child):
        """Doubly link self and child. Overwrites existing parent of child, if any."""
        child.trim()
        child._parent = self
        self._children[id(child)] = child
