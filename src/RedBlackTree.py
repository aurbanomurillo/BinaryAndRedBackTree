from enum import Enum
from typing import Any, Optional


class Color(Enum):
    """Color constants used by Red-Black tree nodes."""

    RED = 0
    BLACK = 1


class RBNode:
    """Node used by the Red-Black tree."""

    def __init__(self, key=None, value=None, color=Color.BLACK, is_nil=False) -> None:
        """
        Initializes a Red-Black tree node.

        Args:
            key: Node key.
            value: Node value.
            color (Color, optional): Node color.
            is_nil (bool, optional): Whether this node is the NIL sentinel.

        Returns:
            None

        Time Complexity:
            O(1)
        """
        self.key = key
        self.data = value
        self.color = color
        self.is_nil = is_nil
        self.parent = None
        self.left = None
        self.right = None

    def is_red(self) -> bool:
        """Checks if the node is red."""
        return self.color == Color.RED

    def is_black(self) -> bool:
        """Checks if the node is black."""
        return self.color == Color.BLACK

    def set_red(self) -> None:
        """Sets the node color to red."""
        self.color = Color.RED

    def set_black(self) -> None:
        """Sets the node color to black."""
        self.color = Color.BLACK

    def get_left(self) -> Optional["RBNode"]:
        """Gets the left child node."""
        return self.left

    def set_left(self, node: Optional["RBNode"]) -> None:
        """Sets the left child node."""
        self.left = node

    def get_right(self) -> Optional["RBNode"]:
        """Gets the right child node."""
        return self.right

    def set_right(self, node: Optional["RBNode"]) -> None:
        """Sets the right child node."""
        self.right = node

    def get_parent(self) -> Optional["RBNode"]:
        """Gets the parent node."""
        return self.parent

    def set_parent(self, node: Optional["RBNode"]) -> None:
        """Sets the parent node."""
        self.parent = node

    def __str__(self) -> str:
        """
        Returns a compact string representation of the node.

        Returns:
            str: "NIL" for sentinel nodes, otherwise "key(C)" where C is the color initial.

        Time Complexity:
            O(1)
        """
        if self.is_nil:
            return "NIL"
        color_str = "R" if self.is_red() else "B"
        return f"{self.key}({color_str})"

    def in_order(self, nil: "RBNode") -> None:
        """
        Prints keys using in-order traversal from this node.

        Args:
            nil (RBNode): Sentinel NIL node.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self == nil:
            return
        self.left.in_order(nil)
        print(self.key, end=" ")
        self.right.in_order(nil)

    def pre_order(self, nil: "RBNode") -> None:
        """
        Prints keys using pre-order traversal from this node.

        Args:
            nil (RBNode): Sentinel NIL node.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self == nil:
            return
        print(self.key, end=" ")
        self.left.pre_order(nil)
        self.right.pre_order(nil)

    def post_order(self, nil: "RBNode") -> None:
        """
        Prints keys using post-order traversal from this node.

        Args:
            nil (RBNode): Sentinel NIL node.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self == nil:
            return
        self.left.post_order(nil)
        self.right.post_order(nil)
        print(self.key, end=" ")

    def show(self, level: int = 0, prefix: str = "Root: ") -> None:
        """
        Displays the node and its subtree with indentation and color.

        Args:
            level (int): Depth level.
            prefix (str): Branch prefix.

        Returns:
            None
        """
        if self.is_nil:
            return
        indent = " " * (level * 4)
        print(f"{indent}{prefix}{self.key} [{self.color.name}]")
        if self.left is not None and not self.left.is_nil:
            self.left.show(level + 1, "L--- ")
        if self.right is not None and not self.right.is_nil:
            self.right.show(level + 1, "R--- ")

    def height(self) -> int:
        """
        Computes the height of the subtree rooted at this node.

        Returns:
            int: Height using node-counting semantics.
        """
        if self.is_nil:
            return 0
        max_height = 0
        stack = [(self, 1)]
        while stack:
            current, depth = stack.pop()
            if depth > max_height:
                max_height = depth
            if current.left is not None and not current.left.is_nil:
                stack.append((current.left, depth + 1))
            if current.right is not None and not current.right.is_nil:
                stack.append((current.right, depth + 1))
        return max_height

    def skew(self) -> bool:
        """
        Checks whether this subtree is balanced by root height difference.

        Returns:
            bool: True if the left/right subtree heights differ by at most 1.
        """
        if self.is_nil:
            return True
        left_height = self.left.height() if self.left is not None and not self.left.is_nil else 0
        right_height = self.right.height() if self.right is not None and not self.right.is_nil else 0
        return right_height - left_height in [-1, 0, 1]

    def search_node(self, key: Any, nil: "RBNode") -> "RBNode":
        """
        Searches and returns the internal RBNode for a key.

        Args:
            key: Key to search.

        Returns:
            RBNode: Matching node or NIL sentinel if not found.

        Time Complexity:
            O(log n)
        """
        current = self
        while current != nil:
            if key == current.key:
                return current
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return nil

class RedBlackTree:
    """Simple Red-Black tree implementation with insertion and deletion fixups."""

    def __init__(self) -> None:
        """
        Initializes an empty Red-Black tree with a shared NIL sentinel.

        Returns:
            None

        Time Complexity:
            O(1)
        """
        self.NIL = RBNode(is_nil=True, color=Color.BLACK)
        self.NIL.parent = self.NIL
        self.NIL.left = self.NIL
        self.NIL.right = self.NIL
        self.root = self.NIL

    def is_empty(self) -> bool:
        """
        Checks whether the tree has no data nodes.

        Returns:
            bool: True if empty, False otherwise.

        Time Complexity:
            O(1)
        """
        return self.root == self.NIL

    def left_rotate(self, pivot_node: "RBNode") -> None:
        """
        Performs a left rotation around the pivot node.

        Args:
            pivot_node (RBNode): Pivot node.

        Returns:
            None

        Time Complexity:
            O(1)
        """
        right_child = pivot_node.right
        pivot_node.right = right_child.left
        if right_child.left != self.NIL:
            right_child.left.parent = pivot_node

        right_child.parent = pivot_node.parent
        if pivot_node.parent == self.NIL:
            self.root = right_child
        elif pivot_node == pivot_node.parent.left:
            pivot_node.parent.left = right_child
        else:
            pivot_node.parent.right = right_child

        right_child.left = pivot_node
        pivot_node.parent = right_child

    def right_rotate(self, pivot_node: "RBNode") -> None:
        """
        Performs a right rotation around the pivot node.

        Args:
            pivot_node (RBNode): Pivot node.

        Returns:
            None

        Time Complexity:
            O(1)
        """
        left_child = pivot_node.left
        pivot_node.left = left_child.right
        if left_child.right != self.NIL:
            left_child.right.parent = pivot_node

        left_child.parent = pivot_node.parent
        if pivot_node.parent == self.NIL:
            self.root = left_child
        elif pivot_node == pivot_node.parent.right:
            pivot_node.parent.right = left_child
        else:
            pivot_node.parent.left = left_child

        left_child.right = pivot_node
        pivot_node.parent = left_child

    def insert(self, key: Any, value: Any = None) -> None:
        """
        Inserts a key/value pair and restores Red-Black properties.

        Args:
            key: Node key.
            value: Optional payload.

        Returns:
            None

        Time Complexity:
            O(log n)
        """
        new_node = RBNode(key, value, color=Color.RED)
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent_node = self.NIL
        current_node = self.root
        while current_node != self.NIL:
            parent_node = current_node
            if new_node.key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right

        new_node.parent = parent_node
        if parent_node == self.NIL:
            self.root = new_node
        elif new_node.key < parent_node.key:
            parent_node.left = new_node
        else:
            parent_node.right = new_node

        self.insert_fixup(new_node)

    def insert_fixup(self, inserted_node: RBNode) -> None:
        """
        Restores Red-Black invariants after insertion.

        Args:
            inserted_node (RBNode): Newly inserted node.

        Returns:
            None

        Time Complexity:
            O(log n)
        """
        while inserted_node.parent.color == Color.RED:
            parent_node = inserted_node.parent
            grandparent_node = parent_node.parent
            if parent_node == grandparent_node.left:
                uncle_node = grandparent_node.right
                if uncle_node.color == Color.RED:
                    parent_node.color = Color.BLACK
                    uncle_node.color = Color.BLACK
                    grandparent_node.color = Color.RED
                    inserted_node = grandparent_node
                else:
                    if inserted_node == parent_node.right:
                        inserted_node = parent_node
                        self.left_rotate(inserted_node)
                    inserted_node.parent.color = Color.BLACK
                    inserted_node.parent.parent.color = Color.RED
                    self.right_rotate(inserted_node.parent.parent)
            else:
                uncle_node = grandparent_node.left
                if uncle_node.color == Color.RED:
                    parent_node.color = Color.BLACK
                    uncle_node.color = Color.BLACK
                    grandparent_node.color = Color.RED
                    inserted_node = grandparent_node
                else:
                    if inserted_node == parent_node.left:
                        inserted_node = parent_node
                        self.right_rotate(inserted_node)
                    inserted_node.parent.color = Color.BLACK
                    inserted_node.parent.parent.color = Color.RED
                    self.left_rotate(inserted_node.parent.parent)

        self.root.color = Color.BLACK
        self.root.parent = self.NIL

    def search_node(self, key: Any) -> "RBNode":
        """
        Searches and returns the internal RBNode for a key.

        Args:
            key: Key to search.

        Returns:
            RBNode: Matching node or NIL sentinel if not found.

        Time Complexity:
            O(log n)
        """
        return self.root.search_node(key, self.NIL)

    def find_node(self, key: Any) -> tuple[Any, Any] | None:
        """
        Searches for a key and returns a public result.

        Args:
            key: Key to search.
            nil
        Returns:
            tuple | None: (key, value) if found; otherwise None.

        Time Complexity:
            O(log n)
        """
        searched_node = self.search_node(key)
        if searched_node == self.NIL:
            return None
        return searched_node.key, searched_node.data

    def minimum(self, node: "RBNode") -> "RBNode":
        """
        Returns the minimum node in a subtree.

        Args:
            node (RBNode): Subtree root.

        Returns:
            RBNode: Minimum-key node in subtree.

        Time Complexity:
            O(log n)
        """
        current_node = node
        while current_node.left != self.NIL:
            current_node = current_node.left
        return current_node

    def transplant(self, node_to_replace: "RBNode", replacement_subtree_root: "RBNode") -> None:
        """
        Replaces subtree rooted at u with subtree rooted at v.

        Args:
            node_to_replace (RBNode): Node to replace.
            replacement_subtree_root (RBNode): Replacement subtree root.

        Returns:
            None

        Time Complexity:
            O(1)
        """
        if node_to_replace.parent == self.NIL:
            self.root = replacement_subtree_root
        elif node_to_replace == node_to_replace.parent.left:
            node_to_replace.parent.left = replacement_subtree_root
        else:
            node_to_replace.parent.right = replacement_subtree_root
        replacement_subtree_root.parent = node_to_replace.parent

    def delete(self, key: Any) -> bool:
        """
        Deletes a key from the Red-Black tree.

        Args:
            key: Key to remove.

        Returns:
            bool: True if key existed and was removed; False otherwise.

        Time Complexity:
            O(log n)
        """
        target_node = self.search_node(key)
        if target_node == self.NIL:
            return False

        node_to_remove = target_node
        original_color = node_to_remove.color

        if node_to_remove.left == self.NIL:
            replacement_node = node_to_remove.right
            self.transplant(node_to_remove, node_to_remove.right)
        elif node_to_remove.right == self.NIL:
            replacement_node = node_to_remove.left
            self.transplant(node_to_remove, node_to_remove.left)
        else:
            successor_node = self.minimum(node_to_remove.right)
            original_color = successor_node.color
            replacement_node = successor_node.right
            if successor_node.parent == node_to_remove:
                replacement_node.parent = successor_node
            else:
                self.transplant(successor_node, successor_node.right)
                successor_node.right = node_to_remove.right
                successor_node.right.parent = successor_node

            self.transplant(node_to_remove, successor_node)
            successor_node.left = node_to_remove.left
            successor_node.left.parent = successor_node
            successor_node.color = node_to_remove.color

        if original_color == Color.BLACK:
            self.delete_fixup(replacement_node)

        if self.root != self.NIL:
            self.root.parent = self.NIL
        return True

    def delete_fixup(self, replacement_node: "RBNode") -> None:
        """
        Restores Red-Black invariants after deletion.

        Args:
            replacement_node (RBNode): Node used as fix-up starting point.

        Returns:
            None

        Time Complexity:
            O(log n)
        """
        while replacement_node != self.root and replacement_node.color == Color.BLACK:
            parent_node = replacement_node.parent
            if replacement_node == parent_node.left:
                sibling_node = parent_node.right
                if sibling_node.color == Color.RED:
                    sibling_node.color = Color.BLACK
                    parent_node.color = Color.RED
                    self.left_rotate(parent_node)
                    sibling_node = parent_node.right

                if sibling_node.left.color == Color.BLACK and sibling_node.right.color == Color.BLACK:
                    sibling_node.color = Color.RED
                    replacement_node = parent_node
                else:
                    if sibling_node.right.color == Color.BLACK:
                        sibling_node.left.color = Color.BLACK
                        sibling_node.color = Color.RED
                        self.right_rotate(sibling_node)
                        sibling_node = parent_node.right

                    sibling_node.color = parent_node.color
                    parent_node.color = Color.BLACK
                    sibling_node.right.color = Color.BLACK
                    self.left_rotate(parent_node)
                    replacement_node = self.root
            else:
                sibling_node = parent_node.left
                if sibling_node.color == Color.RED:
                    sibling_node.color = Color.BLACK
                    parent_node.color = Color.RED
                    self.right_rotate(parent_node)
                    sibling_node = parent_node.left

                if sibling_node.right.color == Color.BLACK and sibling_node.left.color == Color.BLACK:
                    sibling_node.color = Color.RED
                    replacement_node = parent_node
                else:
                    if sibling_node.left.color == Color.BLACK:
                        sibling_node.right.color = Color.BLACK
                        sibling_node.color = Color.RED
                        self.left_rotate(sibling_node)
                        sibling_node = parent_node.left

                    sibling_node.color = parent_node.color
                    parent_node.color = Color.BLACK
                    sibling_node.left.color = Color.BLACK
                    self.right_rotate(parent_node)
                    replacement_node = self.root

        replacement_node.color = Color.BLACK

    def show(self) -> None:
        """
        Prints a hierarchical view of the tree including node colors.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            print("(empty)")
            return
        self.root.show()

    def in_order(self) -> None:
        """
        Prints keys in in-order sequence.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return
        self.root.in_order(self.NIL)
        print()

    def pre_order(self) -> None:
        """
        Prints keys in pre-order sequence.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return
        self.root.pre_order(self.NIL)
        print()

    def post_order(self) -> None:
        """
        Prints keys in post-order sequence.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return
        self.root.post_order(self.NIL)
        print()

    def level_order(self) -> None:
        """
        Prints keys level by level from top to bottom.

        Returns:
            None

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            print(node.key, end=" ")
            if node.left != self.NIL:
                queue.append(node.left)
            if node.right != self.NIL:
                queue.append(node.right)
        print()

    def height(self) -> int:
        """
        Computes tree height (node-counting semantics).

        Returns:
            int: 0 for empty tree, otherwise >= 1.

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return 0
        return self.root.height()

    def skew(self) -> bool:
        """
        Checks whether root balance is within [-1, 0, 1].

        Returns:
            bool: True if root is balanced by this criterion.

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return True
        return self.root.skew()

    def count_nodes_tree(self) -> int:
        """
        Counts all nodes in the tree.

        Returns:
            int: Number of data nodes.

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return 0
        count = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            count += 1
            if node.left != self.NIL:
                stack.append(node.left)
            if node.right != self.NIL:
                stack.append(node.right)
        return count

    def count_leafs(self) -> int:
        """
        Counts leaf nodes (nodes with no children).

        Returns:
            int: Number of leaf nodes.

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return 0
        leafs = 0
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node.left == self.NIL and node.right == self.NIL:
                leafs += 1
                continue
            if node.left != self.NIL:
                stack.append(node.left)
            if node.right != self.NIL:
                stack.append(node.right)
        return leafs

    def longest_path(self) -> list["RBNode"]:
        """
        Returns one longest path from leaf to root.

        Returns:
            list[RBNode]: Leaf-to-root path.

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return []

        deepest_node = self.root
        deepest_depth = 0
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            if node.left == self.NIL and node.right == self.NIL and depth > deepest_depth:
                deepest_depth = depth
                deepest_node = node
            if node.right != self.NIL:
                stack.append((node.right, depth + 1))
            if node.left != self.NIL:
                stack.append((node.left, depth + 1))

        path = []
        current = deepest_node
        while current != self.NIL:
            path.append(current)
            current = current.parent
        return path

    def average_depth(self) -> float:
        """
        Computes average depth of all nodes from the root.

        Returns:
            float: Mean depth (0.0 for empty tree).

        Time Complexity:
            O(n)
        """
        if self.root == self.NIL:
            return 0.0

        depth_sum = 0
        total = 0
        stack = [(self.root, 0)]
        while stack:
            node, depth = stack.pop()
            total += 1
            depth_sum += depth
            if node.left != self.NIL:
                stack.append((node.left, depth + 1))
            if node.right != self.NIL:
                stack.append((node.right, depth + 1))

        return depth_sum / total

    def paths_to_leaf_with_length(self, target_edges: int) -> list[list[str]]:
        """
        Returns all root-to-leaf paths with exact edge length.

        Args:
            target_edges (int): Required number of edges from root to leaf.

        Returns:
            list[list[str]]: Valid paths as key strings.

        Time Complexity:
            O(n)
        """
        return paths_to_leaf_with_length(self.root, target_edges)


def paths_to_leaf_with_length(
    node: Optional["RBNode"],
    remaining_edges: int,
    current_path: Optional[list[str]] = None,
    results: Optional[list[list[str]]] = None,
) -> list[list[str]]:
    """
    Returns all root-to-leaf paths with exact target length in edges.

    Args:
        node (RBNode | None): Current node in DFS (starts at tree root).
        remaining_edges (int): Number of edges still required.
        current_path (list[str] | None, optional): Internal path accumulator.
        results (list[list[str]] | None, optional): Internal valid paths accumulator.

    Returns:
        list[list[str]]: Valid root-to-leaf paths as string keys.

    Time Complexity:
        O(n)
    """
    if current_path is None:
        current_path = []
    if results is None:
        results = []

    if node is None or node.is_nil or remaining_edges < 0:
        return results

    current_path.append(str(node.key))

    left_child = node.get_left()
    right_child = node.get_right()
    left_is_leaf_end = left_child is None or left_child.is_nil
    right_is_leaf_end = right_child is None or right_child.is_nil

    if left_is_leaf_end and right_is_leaf_end:
        if remaining_edges == 0:
            results.append(current_path.copy())
        current_path.pop()
        return results

    paths_to_leaf_with_length(left_child, remaining_edges - 1, current_path, results)
    paths_to_leaf_with_length(right_child, remaining_edges - 1, current_path, results)

    current_path.pop()
    return results


def in_order(tree: RedBlackTree) -> None:
    """Compatibility wrapper for in-order traversal."""
    tree.in_order()


def pre_order(tree: RedBlackTree) -> None:
    """Compatibility wrapper for pre-order traversal."""
    tree.pre_order()


def post_order(tree: RedBlackTree) -> None:
    """Compatibility wrapper for post-order traversal."""
    tree.post_order()


def level_order(tree: RedBlackTree) -> None:
    """Compatibility wrapper for level-order traversal."""
    tree.level_order()


if __name__ == "__main__":
    print("=" * 60)
    print("RedBlackTree basic main test")
    print("=" * 60)

    tree = RedBlackTree()
    for k in [20, 10, 30, 5, 15, 25, 35]:
        tree.insert(k, f"n{k}")

    print("Expected root color: Color.BLACK | Obtained:", tree.root.color)
    print("Expected find_node(25): (25, 'n25') | Obtained:", tree.find_node(25))
    print("Expected count_nodes_tree: 7 | Obtained:", tree.count_nodes_tree())
    print("Expected count_leafs >= 2 | Obtained:", tree.count_leafs())
    print("Expected height <= 7 | Obtained:", tree.height())
    print("Expected average_depth > 0 | Obtained:", round(tree.average_depth(), 3))

    longest = [str(n.key) for n in tree.longest_path()]
    print("longest_path (leaf->root):", longest)
    target = max(0, len(longest) - 1)
    paths = tree.paths_to_leaf_with_length(target)
    print(f"Expected >= 1 path for length {target} | Obtained:", len(paths))

    print("In-order expected: 5 10 15 20 25 30 35")
    print("Obtained: ", end="")
    tree.in_order()

    print("Delete existing key (30) expected True | Obtained:", tree.delete(30))
    print("Delete missing key (999) expected False | Obtained:", tree.delete(999))
    print("Skew bool at root | Obtained:", tree.skew())

