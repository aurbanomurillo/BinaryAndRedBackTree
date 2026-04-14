import os


def _is_red_color(color_value) -> bool:
    """Returns True when a Red-Black node color value represents red."""
    if hasattr(color_value, "name"):
        return color_value.name == "RED"
    return str(color_value).lower() == "red"


def _short_label(value, max_len=14) -> str:
    """Builds a shortened label for plotting nodes."""
    text = str(value)
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."


def _hierarchy_positions(edges, root_id) -> dict:
    """Computes simple layered positions for a tree-like directed graph."""
    children = {}
    for parent, child in edges:
        children.setdefault(parent, []).append(child)

    levels = {}
    stack = [(root_id, 0)]
    seen = set()
    while stack:
        node, depth = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        levels.setdefault(depth, []).append(node)
        for child in children.get(node, []):
            stack.append((child, depth + 1))

    pos = {}
    max_depth = max(levels.keys()) if levels else 0
    for depth, nodes in levels.items():
        n = len(nodes)
        for i, node in enumerate(nodes):
            x = 0.5 if n == 1 else i / (n - 1)
            y = 1.0 - (depth / (max_depth + 1 if max_depth + 1 > 0 else 1))
            pos[node] = (x, y)
    return pos


def plot_binary_tree(tree, output_path, title="Binary Tree", max_layers=6) -> bool:
    """Plots a BinaryTree and saves it as PNG using matplotlib + networkx."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    if tree.root is None:
        return False

    graph = nx.DiGraph()
    queue = [(tree.root, 0)]
    edges = []
    max_allowed_depth = max_layers - 1

    while queue:
        node, depth = queue.pop(0)
        node_id = id(node)
        graph.add_node(node_id, label=_short_label(node.key), color="#6FA8DC")

        left = node.get_left()
        right = node.get_right()
        if left is not None and depth < max_allowed_depth:
            left_id = id(left)
            graph.add_node(left_id, label=_short_label(left.key), color="#6FA8DC")
            graph.add_edge(node_id, left_id)
            edges.append((node_id, left_id))
            queue.append((left, depth + 1))
        if right is not None and depth < max_allowed_depth:
            right_id = id(right)
            graph.add_node(right_id, label=_short_label(right.key), color="#6FA8DC")
            graph.add_edge(node_id, right_id)
            edges.append((node_id, right_id))
            queue.append((right, depth + 1))

    pos = _hierarchy_positions(edges, id(tree.root))
    labels = nx.get_node_attributes(graph, "label")
    colors = [graph.nodes[n].get("color", "#6FA8DC") for n in graph.nodes()]

    plt.figure(figsize=(12, 7))
    nx.draw(
        graph,
        pos=pos,
        labels=labels,
        node_color=colors,
        node_size=900,
        arrows=False,
        font_size=8,
    )
    plt.title(title)
    plt.axis("off")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=140)
    plt.close()
    return True


def plot_red_black_tree(tree, output_path, title="Red-Black Tree", max_layers=6) -> bool:
    """Plots a RedBlackTree and saves it as PNG using matplotlib + networkx."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    if tree.root == tree.NIL:
        return False

    graph = nx.DiGraph()
    queue = [(tree.root, 0)]
    edges = []
    max_allowed_depth = max_layers - 1

    while queue:
        node, depth = queue.pop(0)
        node_id = id(node)
        color = "#E06666" if _is_red_color(node.color) else "#3C3C3C"
        graph.add_node(node_id, label=_short_label(node.key), color=color)

        left = node.left
        right = node.right
        if left != tree.NIL and depth < max_allowed_depth:
            left_id = id(left)
            left_color = "#E06666" if _is_red_color(left.color) else "#3C3C3C"
            graph.add_node(left_id, label=_short_label(left.key), color=left_color)
            graph.add_edge(node_id, left_id)
            edges.append((node_id, left_id))
            queue.append((left, depth + 1))
        if right != tree.NIL and depth < max_allowed_depth:
            right_id = id(right)
            right_color = "#E06666" if _is_red_color(right.color) else "#3C3C3C"
            graph.add_node(right_id, label=_short_label(right.key), color=right_color)
            graph.add_edge(node_id, right_id)
            edges.append((node_id, right_id))
            queue.append((right, depth + 1))

    pos = _hierarchy_positions(edges, id(tree.root))
    labels = nx.get_node_attributes(graph, "label")
    colors = [graph.nodes[n].get("color", "#3C3C3C") for n in graph.nodes()]

    plt.figure(figsize=(12, 7))
    nx.draw(
        graph,
        pos=pos,
        labels=labels,
        node_color=colors,
        node_size=900,
        arrows=False,
        font_size=8,
        font_color="white",
    )
    plt.title(title)
    plt.axis("off")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=140)
    plt.close()
    return True
