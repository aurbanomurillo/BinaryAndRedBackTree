class Node:
    """
    Represents a node in a binary search tree.

    Each node stores a key, optional data, and references to its parent
    and children.
    """

    def __init__(self, key, value=None):
        """
        Initializes a new Node with a key and an optional value.

        Args:
            key: Unique identifier for the node.
            value: Additional data associated with the node.

        Time Complexity:
            O(1)
        """

        self._parent = None
        self._left = None
        self._right = None
        self.key = key
        self.data = value

    def get_left(self):
        """
        Retrieves the left child of the node.

        Returns:
            Node: The left child node.
                Returns None if it does not exist.

        Time Complexity:
            O(1)
        """

        return self._left

    def set_left(self, node):
        """
        Sets the left child of the node and updates the parent reference.

        Args:
            node (Node | None): The node to set as left child, or None to remove.

        Returns:
            None

        Time Complexity:
            O(1)
        """

        self._left = node
        if node is not None:
            node.set_parent(self)

    def get_right(self):
        """
        Retrieves the right child of the node.

        Returns:
            Node: The right child node.
                Returns None if it does not exist.

        Time Complexity:
            O(1)
        """

        return self._right

    def set_right(self, node):
        """
        Sets the right child of the node and updates the parent reference.

        Args:
            node (Node | None): The node to set as right child, or None to remove.

        Returns:
            None

        Time Complexity:
            O(1)
        """

        self._right = node
        if node is not None:
            node.set_parent(self)

    def get_parent(self):
        """
        Retrieves the parent of the node.

        Returns:
            Node: The parent node.
                Returns None if this is the root.

        Time Complexity:
            O(1)
        """

        return self._parent

    def set_parent(self, node):
        """
        Sets the parent of the node.

        Args:
            node (Node | None): The node to set as parent, or None if this becomes the root.

        Returns:
            None

        Time Complexity:
            O(1)
        """

        self._parent = node

    def __str__(self):
        """
        Returns a string representation of the node (its key).

        Returns:
            str: String representation of the node's key.

        Time Complexity:
            O(1)
        """

        return f"{self.key}"

    def show(self, level=0, prefix="Root: "):
        """
        Displays the node and its subtree with indentation and tree structure.

        Prints the node's key with a hierarchical visualization using indentation
        and prefixes (L--- for left child, R--- for right child).

        Args:
            level (int, optional): Current depth level in the tree (default is 0 for root).
            prefix (str, optional): Prefix label for the node (default is "Root: ").

        Returns:
            None

        Time Complexity:
            O(n)
        """

        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if self.get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")
    
    def is_left(self):
        """
        Checks if the current node is the left child of its parent.

        Returns:
            bool: True if this node is the left child of its parent, False otherwise.

        Time Complexity:
            O(1)
        """

        try:
            return self.key == self.get_parent().get_left().key
        except (AttributeError, TypeError):
            return False

    def is_right(self):
        """
        Checks if the current node is the right child of its parent.

        Returns:
            bool: True if this node is the right child of its parent, False otherwise.

        Time Complexity:
            O(1)
        """

        try:
            return self.key == self.get_parent().get_right().key
        except (AttributeError, TypeError):
            return False

    def find_node(self, key):
        """
        Searches for a node with the given key in the current subtree.

        Performs a binary search traversal following BST property:
        - Goes left if key is smaller than current node's key
        - Goes right if key is larger than current node's key

        Args:
            key: Key to search for.

        Returns:
            Node: The node with the matching key if found.
                Returns None otherwise.

        Time Complexity:
            O(log n) average case
            O(n) worst case (completely unbalanced tree)
        """

        if self.key == key:
            return self
        elif key < self.key and self.get_left() is not None:
            return self.get_left().find_node(key)
        elif key > self.key and self.get_right() is not None:
            return self.get_right().find_node(key)
        return None
    
    def min_key(self):
        """
        Finds the node with the minimum key in the current subtree.

        Traverses left until reaching the leftmost node.

        Returns:
            Node: The leftmost (minimum) node in this subtree.

        Time Complexity:
            O(h) - Height of the tree.
        """

        current = self
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def max_key(self):
        """
        Finds the node with the maximum key in the current subtree.

        Traverses right until reaching the rightmost node.

        Returns:
            Node: The rightmost (maximum) node in this subtree.

        Time Complexity:
            O(h) - Height of the tree.
        """

        current = self
        while current.get_right() is not None:
            current = current.get_right()
        return current

    def successor(self):
        """
        Finds the in-order successor of the current node.

        The in-order successor is the next node when performing an in-order
        traversal. It is the minimum node in the right subtree, or the first
        ancestor that has this node in its left subtree.

        Returns:
            Node: The in-order successor node.
                Returns None if no successor exists (this is the maximum).

        Time Complexity:
            O(h) - Height of the tree.
        """

        if self.get_right() is not None:
            return self.get_right().min_key()
        current = self
        parent = self.get_parent()
        while parent is not None and current == parent.get_right():
            current = parent
            parent = parent.get_parent()
        return parent

    def predecessor(self):
        """
        Finds the in-order predecessor of the current node.

        The in-order predecessor is the previous node when performing an in-order
        traversal. It is the maximum node in the left subtree, or the first
        ancestor that has this node in its right subtree.

        Returns:
            Node: The in-order predecessor node.
                Returns None if no predecessor exists (this is the minimum).

        Time Complexity:
            O(h) - Height of the tree.
        """

        if self.get_left() is not None:
            return self.get_left().max_key()
        current = self
        parent = self.get_parent()
        while parent is not None and current == parent.get_left():
            current = parent
            parent = parent.get_parent()
        return parent
    
    def height(self):
        """
        Computes the height of this node (node-counting semantics).

        Height is defined as 1 (for the node itself) plus the maximum height
        of its children. A leaf node has height 1, and a None child has height 0.

        Returns:
            int: Height of this subtree (minimum 1 for a leaf).

        Time Complexity:
            O(n)
        """

        left_height = 0 if self.get_left() is None else self.get_left().height()
        right_height = 0 if self.get_right() is None else self.get_right().height()
        return 1 + max([left_height, right_height])



