from typing import Optional


class Node:
    """
    Represents a node in a binary search tree.

    Each node stores a key, optional data, and references to its parent
    and children.
    """

    def __init__(self, key, value=None) -> None:
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

    def get_left(self) -> Optional["Node"]:
        """
        Retrieves the left child of the node.

        Returns:
            Node: The left child node.
                Returns None if it does not exist.

        Time Complexity:
            O(1)
        """

        return self._left

    def set_left(self, node: Optional["Node"]) -> None:
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

    def get_right(self) -> Optional["Node"]:
        """
        Retrieves the right child of the node.

        Returns:
            Node: The right child node.
                Returns None if it does not exist.

        Time Complexity:
            O(1)
        """

        return self._right

    def set_right(self, node: Optional["Node"]) -> None:
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

    def get_parent(self) -> Optional["Node"]:
        """
        Retrieves the parent of the node.

        Returns:
            Node: The parent node.
                Returns None if this is the root.

        Time Complexity:
            O(1)
        """

        return self._parent

    def set_parent(self, node: Optional["Node"]) -> None:
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

    def __str__(self) -> str:
        """
        Returns a string representation of the node (its key).

        Returns:
            str: String representation of the node's key.

        Time Complexity:
            O(1)
        """

        return f"{self.key}"

    def show(self, level=0, prefix="Root: ") -> None:
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

    def is_left(self) -> bool:
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

    def is_right(self) -> bool:
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

    def find_node(self, key) -> Optional["Node"]:
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

    def min_key(self) -> "Node":
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

    def max_key(self) -> "Node":
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

    def successor(self) -> Optional["Node"]:
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

    def predecessor(self) -> Optional["Node"]:
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

    def height(self) -> int:
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

    def count(self) -> int:
        """
        Counts all nodes in the subtree rooted at this node.

        Returns:
            int: Total number of nodes in this subtree.

        Time Complexity:
            O(n)
        """
        left = 0 if self.get_left() is None else self.get_left().count()
        right = 0 if self.get_right() is None else self.get_right().count()
        return 1 + left + right

    def count_leafs(self) -> int:
        """
        Counts how many leaf nodes exist in this subtree.

        A leaf is a node with no left and no right child.

        Returns:
            int: Number of leaf nodes in this subtree.

        Time Complexity:
            O(n)
        """
        if self.get_left() is None and self.get_right() is None:
            return 1
        elif self.get_left() is None:
            return self.get_right().count_leafs()
        elif self.get_right() is None:
            return self.get_left().count_leafs()
        return self.get_right().count_leafs() + self.get_left().count_leafs()

    def longest_from_node(self) -> list["Node"]:
        """
        Returns one longest path from a leaf up to this node.

        In case of ties, the left subtree path is preferred.

        Returns:
            list[Node]: Path ordered from leaf to this node.

        Time Complexity:
            O(n)
        """
        left_path = [] if self.get_left() is None else self.get_left().longest_from_node()
        right_path = [] if self.get_right() is None else self.get_right().longest_from_node()
        best_child_path = left_path if len(left_path) >= len(right_path) else right_path
        return best_child_path + [self]

    def skew(self) -> bool:
        """
        Checks root-level balance for this node's subtree.

        A node is considered balanced if the height difference between
        right and left subtrees is in {-1, 0, 1}.

        Returns:
            bool: True if balanced by this criterion, False otherwise.

        Time Complexity:
            O(n)
        """
        if self.get_right() is None:
            right_height = 0
        else:
            right_height = self.get_right().height()

        if self.get_left() is None:
            left_height = 0
        else:
            left_height = self.get_left().height()

        return right_height - left_height in [-1, 0, 1]

class BinaryTree:
    """
    Represents a binary search tree with a reference to its root node.

    Maintains the BST property: for each node, all keys in the left subtree
    are smaller, and all keys in the right subtree are larger.
    """

    def __init__(self, root: Optional[Node] = None) -> None:
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

    def height(self) -> int:
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

    def count_nodes_tree(self) -> int:
        """
        Counts the total number of nodes in the tree.

        Returns:
            int: Total number of nodes in the tree.

        Time Complexity:
            O(n)
        """

        return 0 if self.root is None else self.root.count()

    def count_leafs(self) -> int:
        """
        Counts how many nodes are leaves (nodes with no children).

        Returns:
            int: Number of leaf nodes.

        Time Complexity:
            O(n)
        """

        return 0 if self.root is None else self.root.count_leafs()

    def longest_path(self) -> list:
        """
        Returns one longest path from a leaf to the root.

        Returns:
            list[Node]: Node pointers in the path ordered from leaf to root.

        Time Complexity:
            O(n)
        """

        return [] if self.root is None else self.root.longest_from_node()


def in_order(tree: BinaryTree) -> None:
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

def pre_order(tree: BinaryTree) -> None:
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

def post_order(tree: BinaryTree) -> None:
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

def level_order(tree: BinaryTree) -> None:
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
    node: Optional["Node"],
    remaining_edges: int,
    current_path: Optional[list[str]] =None,
    results: Optional[list[list[str]]] =None,
    ) ->list[list[str]]:    
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


if __name__ == "__main__":
    print("=" * 60)
    print("BinaryTree basic main test")
    print("=" * 60)

    tree = BinaryTree(Node(20, "n20"))
    for k in [10, 30, 5, 15, 25, 35]:
        tree.insert(k, f"n{k}")

    print("Expected root: 20 | Obtained:", tree.root.key)
    print("Expected find_node(25): (25, 'n25') | Obtained:", tree.find_node(25))
    print("Expected count_nodes_tree: 7 | Obtained:", tree.count_nodes_tree())
    print("Expected count_leafs: 4 | Obtained:", tree.count_leafs())

    longest = [str(n.key) for n in tree.longest_path()]
    print("Expected longest_path length: 3 nodes | Obtained:", len(longest))
    print("longest_path (leaf->root):", longest)

    p2 = paths_to_leaf_with_length(tree.root, 2)
    print("Expected paths_to_leaf_with_length(..., 2): 4 paths | Obtained:", len(p2))
    print("paths:", p2)

    print("In-order expected: 5 10 15 20 25 30 35")
    print("Obtained: ", end="")
    in_order(tree)

    deleted = tree.delete(30)
    print("Expected delete(30): True | Obtained:", deleted)
    print("Expected skew bool | Obtained:", tree.skew())

