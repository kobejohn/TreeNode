Quick Usage
===========
    >>> from treenode import TreeNode
    >>> root = TreeNode(attr_1 = 1, attr_2 = 2)
    >>> root
    TreeNode:
        parent: none
        children: 0
        attr_2: 2
        attr_1: 1
    >>> #connect a child to root
    >>> child = TreeNode(attr_3 = 3, attr_4 = 4)
    >>> root.graft_child(child)
    >>> root
    TreeNode:
        parent: none
        children: 1
        attr_2: 2
        attr_1: 1
    >>> child
    TreeNode:
        parent: yes
        children: 0
        attr_3: 3
        attr_4: 4



Introduction
============

Store data in easy to use nodes that provide both data storage and tree behavior.

It supports various tree operations such as:

- separating and combining trees (automatically avoids creating cycles)
- traversing the nodes in-order or post-order
- access up or down through doubly-linked parent/child


I have used it in several projects where I needed storage of iterative
simulation data.

It is currently being reimplemented from old code so there is a lot of
missing functionality.



Copyright
==================
Copyright (c) 2012 John Nieri and contributors under MIT License. See LICENSE
in this repository or distribution for details.