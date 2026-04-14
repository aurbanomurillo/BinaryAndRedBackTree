import os
import random
import sys
from typing import Optional

sys.setrecursionlimit(15000)

from BinaryTree import BinaryTree
from RedBlackTree import RedBlackTree
from plot_utils import plot_binary_tree, plot_red_black_tree


def load_words(file_path: str) -> list[str]:
    """Loads and cleans the word list from disk."""
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def ask_letters(max_letters: int = 3) -> list[str]:
    """Asks the user for up to max_letters letters and returns normalized input."""
    letters: list[str] = []

    print(f"Introduce hasta {max_letters} letras (pulsa Enter para terminar).")
    while len(letters) < max_letters:
        raw = input(f"Letra {len(letters) + 1}: ").strip().lower()
        if raw == "":
            break

        letter = raw[0]
        if not letter.isalpha():
            print("Entrada no valida. Introduce una letra.")
            continue

        letters.append(letter)

    return letters


def ask_insertion_mode() -> str:
    """Asks whether insertion should be default order or randomized order."""
    while True:
        mode = input("Modo de insercion [d=defecto / r=aleatoria]: ").strip().lower()
        if mode in {"d", "r"}:
            return mode
        print("Opcion no valida. Escribe 'd' o 'r'.")


def ask_generate_plots() -> bool:
    """Asks whether optional PNG plots should be generated."""
    while True:
        choice = input("Generar plots opcionales (matplotlib+networkx)? [s/n]: ").strip().lower()
        if choice in {"s", "n"}:
            return choice == "s"
        print("Opcion no valida. Escribe 's' o 'n'.")


def ask_tree_type() -> str:
    """Asks which tree type should be executed."""
    while True:
        tree_type = input("Tipo de arbol [b=binario / r=rojo-negro]: ").strip().lower()
        if tree_type in {"b", "r"}:
            return tree_type
        print("Opcion no valida. Escribe 'b' o 'r'.")


def ask_height() -> int:
    """Asks how many layers should be shown in plots."""
    while True:
        raw_height = input("HEIGHT (capas del arbol): ").strip()
        try:
            height = int(raw_height)
        except ValueError:
            print("Opcion no valida. Introduce un numero entero mayor que 0.")
            continue

        if height > 0:
            return height
        print("Opcion no valida. Introduce un numero entero mayor que 0.")


def build_tree_from_words(words: list[str], randomize: bool) -> BinaryTree:
    """Builds a BinaryTree from the given word list."""
    if not words:
        return BinaryTree(None)

    ordered_words = words[:]
    if randomize:
        random.shuffle(ordered_words)

    if not randomize and _is_non_decreasing(ordered_words):
        tree = BinaryTree(None)
        tree.insert(ordered_words[0], ordered_words[0])
        current = tree.root
        node_cls = type(current)
        for word in ordered_words[1:]:
            new_node = node_cls(word, word)
            current.set_right(new_node)
            current = new_node
        return tree

    tree = BinaryTree(None)
    for word in ordered_words:
        tree.insert(word, word)

    return tree


def build_red_black_tree_from_words(words: list[str], randomize: bool) -> RedBlackTree:
    """Builds a RedBlackTree from the given word list."""
    tree = RedBlackTree()
    if not words:
        return tree

    ordered_words = words[:]
    if randomize:
        random.shuffle(ordered_words)

    for word in ordered_words:
        tree.insert(word, word)

    return tree


def _is_non_decreasing(values: list[str]) -> bool:
    """Checks whether values are in non-decreasing order."""
    for i in range(1, len(values)):
        if values[i] < values[i - 1]:
            return False
    return True


def count_nodes_iterative(root: Optional[object]) -> int:
    """Counts nodes using an iterative DFS to avoid deep recursion."""
    if root is None:
        return 0
    count = 0
    stack = [root]
    while stack:
        node = stack.pop()
        count += 1
        if node.get_left() is not None:
            stack.append(node.get_left())
        if node.get_right() is not None:
            stack.append(node.get_right())
    return count


def count_leafs_iterative(root: Optional[object]) -> int:
    """Counts leaf nodes using an iterative DFS to avoid deep recursion."""
    if root is None:
        return 0
    leafs = 0
    stack = [root]
    while stack:
        node = stack.pop()
        left = node.get_left()
        right = node.get_right()
        if left is None and right is None:
            leafs += 1
            continue
        if left is not None:
            stack.append(left)
        if right is not None:
            stack.append(right)
    return leafs


def longest_path_iterative(root: Optional[object]) -> list[object]:
    """Returns one longest leaf-to-root path using iterative traversal."""
    if root is None:
        return []

    deepest_node = root
    deepest_depth = 0
    stack: list[tuple[object, int]] = [(root, 0)]

    while stack:
        node, depth = stack.pop()
        left = node.get_left()
        right = node.get_right()

        if left is None and right is None and depth > deepest_depth:
            deepest_depth = depth
            deepest_node = node

        if right is not None:
            stack.append((right, depth + 1))
        if left is not None:
            stack.append((left, depth + 1))

    path: list[object] = []
    current = deepest_node
    while current is not None:
        path.append(current)
        current = current.get_parent()
    return path


def paths_to_leaf_with_length_iterative(root: Optional[object], target_edges: int) -> list[list[str]]:
    """Returns all root-to-leaf paths with exact length using iterative DFS."""
    if root is None or target_edges < 0:
        return []

    def _unwind_path(path_ref) -> list[str]:
        """Rebuilds a path list from a backward linked tuple representation."""
        out = []
        current_ref = path_ref
        while current_ref is not None:
            out.append(current_ref[0])
            current_ref = current_ref[1]
        out.reverse()
        return out

    results: list[list[str]] = []
    initial_ref = (str(root.key), None)
    stack = [(root, 0, initial_ref)]

    while stack:
        node, edges, path_ref = stack.pop()
        left = node.get_left()
        right = node.get_right()

        if left is None and right is None:
            if edges == target_edges:
                results.append(_unwind_path(path_ref))
            continue

        if edges >= target_edges:
            continue

        if right is not None:
            stack.append((right, edges + 1, (str(right.key), path_ref)))
        if left is not None:
            stack.append((left, edges + 1, (str(left.key), path_ref)))

    return results


def summarize_sequence(values: list[str], max_items: int = 16) -> list[str]:
    """Summarizes a long sequence for readable console output."""
    if len(values) <= max_items:
        return values
    half = max_items // 2
    return values[:half] + ["..."] + values[-half:]


def get_words_starting_with(all_words: list[str], letter: str) -> list[str]:
    """Returns all words that start with the given letter."""
    return [word for word in all_words if word.startswith(letter)]


def print_tree_report(letter: str, tree: BinaryTree) -> None:
    """Prints the required report for one letter tree."""
    print("\n" + "=" * 60)
    print(f"Letra: {letter}")

    if tree.root is None:
        print("No hay palabras para esta letra.")
        return

    root_word = str(tree.root.key)
    left_word = None if tree.root.get_left() is None else str(tree.root.get_left().key)
    right_word = None if tree.root.get_right() is None else str(tree.root.get_right().key)

    print(f"Palabra en raiz: {root_word}")
    print(f"Palabra en hijo izquierdo de raiz: {left_word}")
    print(f"Palabra en hijo derecho de raiz: {right_word}")
    nodes_count = count_nodes_iterative(tree.root)
    leafs_count = count_leafs_iterative(tree.root)
    print(f"Numero de nodos: {nodes_count}")
    print(f"Numero de hojas: {leafs_count}")

    longest_path_nodes = longest_path_iterative(tree.root)
    longest_path_words = [str(node.key) for node in longest_path_nodes]
    print(f"Ruta mas larga hoja->raiz ({len(longest_path_words)} nodos): {summarize_sequence(longest_path_words)}")

    target_edges = max(0, len(longest_path_words) - 1)
    paths = paths_to_leaf_with_length_iterative(tree.root, target_edges)
    if len(paths) <= 3:
        shown_paths = [summarize_sequence(path) for path in paths]
    else:
        shown_paths = [summarize_sequence(path) for path in paths[:3]]
    print(f"Caminos raiz->hoja con {target_edges} aristas: {len(paths)} encontrados")
    print(f"Vista previa caminos: {shown_paths}")


def print_tree_report_rbt(letter: str, tree: RedBlackTree) -> None:
    """Prints the required report for one letter Red-Black tree."""
    print("\n" + "=" * 60)
    print(f"Letra: {letter}")
    print("Tipo: RedBlackTree")

    if tree.root == tree.NIL:
        print("No hay palabras para esta letra.")
        return

    root_word = str(tree.root.key)
    left_word = None if tree.root.left == tree.NIL else str(tree.root.left.key)
    right_word = None if tree.root.right == tree.NIL else str(tree.root.right.key)

    print(f"Palabra en raiz: {root_word}")
    print(f"Palabra en hijo izquierdo de raiz: {left_word}")
    print(f"Palabra en hijo derecho de raiz: {right_word}")

    nodes_count = tree.count_nodes_tree()
    leafs_count = tree.count_leafs()
    print(f"Numero de nodos: {nodes_count}")
    print(f"Numero de hojas: {leafs_count}")
    print(f"Altura: {tree.height()}")
    print(f"Skew en raiz: {tree.skew()}")
    print(f"Media de profundidad: {round(tree.average_depth(), 3)}")

    longest_path_nodes = tree.longest_path()
    longest_path_words = [str(node.key) for node in longest_path_nodes]
    print(f"Ruta mas larga hoja->raiz ({len(longest_path_words)} nodos): {summarize_sequence(longest_path_words)}")

    target_edges = max(0, len(longest_path_words) - 1)
    paths = tree.paths_to_leaf_with_length(target_edges)
    if len(paths) <= 3:
        shown_paths = [summarize_sequence(path) for path in paths]
    else:
        shown_paths = [summarize_sequence(path) for path in paths[:3]]
    print(f"Caminos raiz->hoja con {target_edges} aristas: {len(paths)} encontrados")
    print(f"Vista previa caminos: {shown_paths}")


def print_comparison(letter: str, bst_tree: BinaryTree, rbt_tree: RedBlackTree) -> None:
    """Prints a compact metric comparison between BST and Red-Black tree."""
    print("\n" + "-" * 60)
    print(f"Comparativa para letra '{letter}'")

    bst_nodes = count_nodes_iterative(bst_tree.root)
    bst_leafs = count_leafs_iterative(bst_tree.root)
    bst_height = 0 if bst_tree.root is None else len(longest_path_iterative(bst_tree.root))

    rbt_nodes = rbt_tree.count_nodes_tree()
    rbt_leafs = rbt_tree.count_leafs()
    rbt_height = rbt_tree.height()

    print(f"Nodos -> BST: {bst_nodes} | RBT: {rbt_nodes}")
    print(f"Hojas -> BST: {bst_leafs} | RBT: {rbt_leafs}")
    print(f"Altura -> BST: {bst_height} | RBT: {rbt_height}")


def generate_plots_for_letter(letter: str, bst_tree: BinaryTree, rbt_tree: RedBlackTree, output_dir: str, max_layers: int) -> None:
    """Generates optional PNG plots for one letter in both tree types."""
    bst_path = os.path.join(output_dir, f"{letter}_bst.png")
    rbt_path = os.path.join(output_dir, f"{letter}_rbt.png")

    bst_ok = plot_binary_tree(bst_tree, bst_path, title=f"BST - letra '{letter}'", max_layers=max_layers)
    rbt_ok = plot_red_black_tree(rbt_tree, rbt_path, title=f"RBT - letra '{letter}'", max_layers=max_layers)

    if bst_ok:
        print(f"Plot BST guardado en: {bst_path}")
    else:
        print("Plot BST no generado (arbol vacio).")

    if rbt_ok:
        print(f"Plot RBT guardado en: {rbt_path}")
    else:
        print("Plot RBT no generado (arbol vacio).")


def generate_plot_bst_for_letter(letter: str, bst_tree: BinaryTree, output_dir: str, max_layers: int) -> None:
    """Generates optional PNG plot for one letter in BST mode."""
    bst_path = os.path.join(output_dir, f"{letter}_bst.png")
    bst_ok = plot_binary_tree(bst_tree, bst_path, title=f"BST - letra '{letter}'", max_layers=max_layers)
    if bst_ok:
        print(f"Plot BST guardado en: {bst_path}")
    else:
        print("Plot BST no generado (arbol vacio).")


def generate_plot_rbt_for_letter(letter: str, rbt_tree: RedBlackTree, output_dir: str, max_layers: int) -> None:
    """Generates optional PNG plot for one letter in RBT mode."""
    rbt_path = os.path.join(output_dir, f"{letter}_rbt.png")
    rbt_ok = plot_red_black_tree(rbt_tree, rbt_path, title=f"RBT - letra '{letter}'", max_layers=max_layers)
    if rbt_ok:
        print(f"Plot RBT guardado en: {rbt_path}")
    else:
        print("Plot RBT no generado (arbol vacio).")


def main() -> None:
    """Main entry point for part 2 of the assessment."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "data", "palabras_RAE_cleaned_noaccents.txt")

    if not os.path.exists(data_file):
        print(f"No se encuentra el fichero de palabras: {data_file}")
        return

    words = load_words(data_file)
    mode = ask_insertion_mode()
    tree_type = ask_tree_type()
    generate_plots = ask_generate_plots()
    HEIGHT = ask_height()
    letters = ask_letters(max_letters=3)

    if not letters:
        print("No se introdujeron letras. Fin del programa.")
        return

    randomize = mode == "r"
    plots_dir = os.path.join(base_dir, "src", "plots")

    for letter in letters:
        letter_words = get_words_starting_with(words, letter)

        if tree_type == "b":
            bst_tree = build_tree_from_words(letter_words, randomize=randomize)
            print_tree_report(letter, bst_tree)
            if generate_plots:
                generate_plot_bst_for_letter(letter, bst_tree, plots_dir, HEIGHT)
        else:
            rbt_tree = build_red_black_tree_from_words(letter_words, randomize=randomize)
            print_tree_report_rbt(letter, rbt_tree)
            if generate_plots:
                generate_plot_rbt_for_letter(letter, rbt_tree, plots_dir, HEIGHT)


if __name__ == "__main__":
    main()
