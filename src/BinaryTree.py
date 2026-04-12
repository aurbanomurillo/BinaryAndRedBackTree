from Node import Node

class BinaryTree:
    """
    Represents a binary search tree with a reference to its root node.

    Maintains the BST property: for each node, all keys in the left subtree
    are smaller, and all keys in the right subtree are larger.
    """

    def __init__(self, root=None):
        """
        Initializes the binary tree with a root node.

        Args:
            root (Node | None, optional): The root node of the binary tree (default is None for empty tree).

        Returns:
            None

        Time Complexity:
            O(1)
        """

        self.root = root

    def insert(self, key, value=None) -> None:
        """
        Inserts a new node with the given key and optional value into the BST.

        Performs iterative BST insertion following the standard algorithm:
        - Compare key with current node
        - Go left if key is smaller, right if larger or equal
        - Insert as leaf when appropriate position is found

        Args:
            key: The key for the new node.
            value: Optional data associated with the key (default is None).

        Returns:
            None

        Time Complexity:
            O(log n) average case (balanced BST)
            O(n) worst case (completely unbalanced tree)
        """

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

    def height(self):
        """
        Computes the height of the entire binary tree.

        Returns 0 for an empty tree, or delegates to root's height method
        which uses node-counting semantics.

        Returns:
            int: Height of the tree (0 for empty, minimum 1 for single node).

        Time Complexity:
            O(n) - Must visit all n nodes in the tree to compute height.
        """
        if self.root is None:
            return 0
        return self.root.height()
    
    def find_node(self, key) -> tuple | None:
        """
        Searches for a node with the given key and returns its data.

        Performs iterative BST search following the standard algorithm.

        Args:
            key: Key to search for.

        Returns:
            tuple: Tuple of (key, data) if found.
                Returns None otherwise.

        Time Complexity:
            O(log n) average case (balanced BST)
            O(n) worst case (completely unbalanced tree)
        """
        current = self.root
        while current is not None:
            if key == current.key:
                return key, current.data
            elif key < current.key:
                current = current.get_left()
            else:
                current = current.get_right()
        return None

    def delete(self, key) -> bool:
        """
        Deletes a node with the given key from the BST.

        Handles three cases:
        1. Leaf node: simply remove
        2. Node with one child: replace with that child
        3. Node with two children: replace with in-order successor, then delete successor

        Args:
            key: Key of the node to delete.

        Returns:
            bool: True if deletion was successful, False if key not found.

        Time Complexity:
            O(log n) average case (balanced BST)
            O(n) worst case (completely unbalanced tree)
        """
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
        """
        Checks if the tree is balanced at the root level.

        Determines if the height difference between left and right subtrees
        of the root is within [-1, 0, 1], which indicates a balanced tree.

        Returns:
            bool: True if the tree is balanced at root (difference in [-1, 0, 1]),
                False if unbalanced (difference outside that range).

        Time Complexity:
            O(n) - Must compute heights of both subtrees (visits all nodes).
        """
        if self.root is None:
            return True
        else:
            return self.root.skew()

    def show(self) -> None:
        """
        Displays the entire binary tree with hierarchical structure.

        Prints a visual representation of the tree using indentation and
        prefixes to show the parent-child relationships.

        Returns:
            None

        Time Complexity:
            O(n) - Visits all n nodes in the tree and prints them.
        """
        if self.root is not None:
            self.root.show()

    def count_nodes_tree(self):
        """
        Counts the total number of nodes in the tree.

        Returns:
            int: Total number of nodes in the tree.

        Time Complexity:
            O(n)
        """

        return 0 if self.root is None else self.root.count()

    def count_leafs(self):
        """
        Counts how many nodes are leaves (nodes with no children).

        Returns:
            int: Number of leaf nodes.

        Time Complexity:
            O(n)
        """

        return 0 if self.root is None else self.root.count_leafs()

    def longest_path(self):
        """
        Returns one longest path from a leaf to the root.

        Returns:
            list[Node]: Node pointers in the path ordered from leaf to root.

        Time Complexity:
            O(n)
        """

        return [] if self.root is None else self.root.longest_from_node()


def in_order(tree) -> None:
    """
    Performs in-order (left-root-right) traversal of the binary tree.

    In-order traversal visits nodes in ascending order when applied to a BST.
    The output is a space-separated list of keys on a single line.

    Args:
        tree (BinaryTree | Node): Either a BinaryTree instance (initial call) or a Node instance (recursive calls).

    Returns:
        None

    Time Complexity:
        O(n) - Visits all n nodes in the tree exactly once.
    """
    if isinstance(tree, BinaryTree):
        if tree.root is None:
            return
        in_order(tree.root)
        print()
    else:
        if tree is None:
            return
        in_order(tree.get_left())
        print(tree.key, end=' ')
        in_order(tree.get_right())

def pre_order(tree) -> None:
    """
    Performs pre-order (root-left-right) traversal of the binary tree.

    Pre-order traversal visits the root before its subtrees. Useful for
    creating a copy of the tree or for serialization.
    The output is a space-separated list of keys on a single line.

    Args:
        tree (BinaryTree | Node): Either a BinaryTree instance (initial call) or a Node instance (recursive calls).

    Returns:
        None

    Time Complexity:
        O(n) - Visits all n nodes in the tree exactly once.
    """
    if isinstance(tree, BinaryTree):
        if tree.root is None:
            return
        pre_order(tree.root)
        print()
    else:
        if tree is None:
            return
        print(tree.key, end=' ')
        pre_order(tree.get_left())
        pre_order(tree.get_right())

def post_order(tree) -> None:
    """
    Performs post-order (left-right-root) traversal of the binary tree.

    Post-order traversal visits the root after its subtrees. Useful for
    deletion, computing subtree properties, or evaluating expressions.
    The output is a space-separated list of keys on a single line.

    Args:
        tree (BinaryTree | Node): Either a BinaryTree instance (initial call) or a Node instance (recursive calls).

    Returns:
        None

    Time Complexity:
        O(n) - Visits all n nodes in the tree exactly once.
    """
    if isinstance(tree, BinaryTree):
        if tree.root is None:
            return
        post_order(tree.root)
        print()
    else:
        if tree is None:
            return
        post_order(tree.get_left())
        post_order(tree.get_right())
        print(tree.key, end=' ')

def level_order(tree) -> None:
    """
    Performs level-order (breadth-first) traversal of the binary tree.

    Level-order traversal processes the tree level by level, from top to bottom,
    and from left to right within each level. Uses a queue-based iterative approach
    without external data structure imports (uses list with pop(0)).
    The output is a space-separated list of keys on a single line.

    Args:
        tree (BinaryTree): The binary tree to traverse.

    Returns:
        None

    Time Complexity:
        O(n) - Visits all n nodes in the tree exactly once.
        Space Complexity: O(w) where w is the maximum width (number of nodes at widest level).
    """
    if tree.root is None:
        return
    queue = [tree.root]
    while queue:
        node = queue.pop(0)
        print(node.key, end=' ')
        if node.get_left() is not None:
            queue.append(node.get_left())
        if node.get_right() is not None:
            queue.append(node.get_right())
    print()

def paths_to_leaf_with_length(
        node: Node, remaining_edges: int, 
        current_path: list[str] = None, 
        results: list[list[str]] = None
        ) -> list[list[str]]:
    
    """
    Returns all root-to-leaf paths with exact target length in edges.

    The target length is given by ``remaining_edges`` at the beginning of the
    call. This function uses backtracking to explore both subtrees while
    building a current path and collecting only valid paths.

    Typical usage:
        paths = paths_to_leaf_with_length(tree.root, 3)

    Args:
        node (Node | None): Current node in the DFS traversal (starts at root).
        remaining_edges (int): Number of edges still required to reach
            the target length.
        current_path (list[str] | None, optional): Internal path accumulator
            for the current DFS branch.
        results (list[list[str]] | None, optional): Internal accumulator of
            valid paths.

    Returns:
        list[list[str]]: List of valid paths. Each path is a list of
            strings built as ``str(node.key)``.

    Time Complexity:
        O(n) - Visits each node at most once in the traversal.
    """
    if current_path is None:
        current_path = []
    if results is None:
        results = []

    if node is None:
        return results

    current_path.append(str(node.key))

    if node.get_left() is None and node.get_right() is None:
        if remaining_edges == 0:
            results.append(current_path.copy())
        current_path.pop()
        return results

    if remaining_edges > 0:
        paths_to_leaf_with_length(node.get_left(), remaining_edges - 1, current_path, results)
        paths_to_leaf_with_length(node.get_right(), remaining_edges - 1, current_path, results)

    current_path.pop()
    return results

