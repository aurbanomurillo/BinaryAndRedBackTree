class Node:
    """
    Represents a node in a binary search tree.

    Each node stores a key, optional data, and references to its parent
    and children.
    """

    def __init__(self, key, value=None):
        """
        Initializes a new Node with a key and an optional value.

        Parameters:
        ----------
        key : any
            Unique identifier for the node.
        value : any, optional
            Additional data associated with the node.
        """
        self._parent = None  # Pointer to the parent node
        self._left = None    # Pointer to the left child
        self._right = None   # Pointer to the right child
        self.key = key       # Key that identifies the node
        self.data = value    # Optional additional data

    def get_left(self) -> 'Node':
        """
        Retrieves the left child of the node.

        Returns:
        -------
        Node or None
        """
        return self._left

    def set_left(self, node) -> None:
        """
        Sets the left child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._left = node
        if node is not None:
            node.set_parent(self)

    def get_right(self) -> 'Node':
        """
        Retrieves the right child of the node.

        Returns:
        -------
        Node or None
        """
        return self._right

    def set_right(self, node) -> None:
        """
        Sets the right child of the node and updates the parent reference.

        Parameters:
        ----------
        node : Node
        """
        self._right = node
        if node is not None:
            node.set_parent(self)

    def get_parent(self) -> 'Node':
        """
        Retrieves the parent of the node.

        Returns:
        -------
        Node or None
        """
        return self._parent

    def set_parent(self, node) -> None:
        """
        Sets the parent of the node.

        Parameters:
        ----------
        node : Node
        """
        self._parent = node

    def __str__(self):
        """
        Returns a string representation of the node (its key).
        """
        return f"{self.key}"

    def show(self, level=0, prefix="Root: ") -> None:
        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self}")

        if self.get_left() is not None:
            self.get_left().show(level + 1, prefix="L--- ")
        if self.get_right() is not None:
            self.get_right().show(level + 1, prefix="R--- ")
    
    def is_right(self) -> bool:
        try: return self.key == self.get_parent().get_right().key
        except: return False

    def is_right(self) -> bool:
        try: return self.key == self.get_parent().get_left().key
        except: return False
    
    def find_node(self, key) -> 'Node':
        """
        Searches for a node with the given key in the current subtree.

        Parameters:
        ----------
        key : any
            Key to search for.

        Returns:
        -------
        Node or None
            Matching node if found, otherwise None.
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

        Returns:
        -------
        Node
            Leftmost node in this subtree.
        """
        current = self
        while current.get_left() is not None:
            current = current.get_left()
        return current

    def max_key(self):
        """
        Finds the node with the maximum key in the current subtree.

        Returns:
        -------
        Node
            Rightmost node in this subtree.
        """
        current = self
        while current.get_right() is not None:
            current = current.get_right()
        return current

    def successor(self):
        """
        Finds the in-order successor of the current node.

        Returns:
        -------
        Node or None
            Next node in sorted order, or None if it does not exist.
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

        Returns:
        -------
        Node or None
            Previous node in sorted order, or None if it does not exist.
        """
        if self.get_left() is not None:
            return self.get_left().max_key()
        current = self
        parent = self.get_parent()
        while parent is not None and current == parent.get_left():
            current = parent
            parent = parent.get_parent()
        return parent
    
    def height(self) -> int:
        left_height = 0 if self.get_left() is None else self.get_left().height()
        right_height = 0 if self.get_right() is None else self.get_right().height()

        return 1 + max([left_height, right_height])

class BinaryTree:
    """
    Represents a binary search tree with a reference to its root node.
    """

    def __init__(self, root: Node):
        """
        Initializes the binary tree with a root node.

        Parameters:
        ----------
        root : Node
            The root node of the binary tree.
        """
        self.root = root

    def insert(self, key, value=None) -> None:
        new_node = Node(key, value)
        if self.root is None:
            self.root = new_node
        else:
            current = self.root
            cond = True
            while cond:
                if key < current.key:
                    if current.get_left() is None:
                        current.set_left(new_node)
                        cond = False
                    else:
                        current = current.get_left()
                else:
                    if current.get_right() is None:
                        current.set_right(new_node)
                        cond = False
                    else:
                        current = current.get_right()
    def height(self) -> None:
        if self.root == None: return 0
        return self.root.height()
    
    def find_node(self, key) -> tuple:
        current = self.root
        while True:
            if key == current.key: return key, current.data
            elif key < current.key:
                if current.get_left() is None: return None
                else: current = current.get_left()
            else:
                if current.get_right() is None: return None
                else: current = current.get_right()

    def delete(self, key) -> bool:
        if self.root is None:
            return False
        current = self.root
        while current is not None and not current.key == key:
            if key < current.key:
                current = current.get_left()
            else:
                current = current.get_right()
        if current is None:
            return False
        if current.get_left() is not None and current.get_right() is not None:
            succ = current.successor()
            current.key = succ.key
            current.data = succ.data
            current = succ
        child = current.get_left() if current.get_left() is not None else current.get_right()
        parent = current.get_parent()
        if parent is None:
            self.root = child
            if child is not None:
                child.set_parent(None)
        elif parent.get_left() == current:
            parent.set_left(child)
        else:
            parent.set_right(child)
        return True

    def skew(self) -> bool:
        if self.root == None:
            return True
        if self.root.get_right() is None:
            right_height = 0
        else:
            right_height = self.root.get_right().height()
        if self.root.get_left() is None:
            left_height = 0
        else:
            left_height = self.root.get_left().height()
        return right_height - left_height in [-1, 0, 1]

    def show(self) -> None:
        """Displays the entire binary tree."""
        self.root.show()





