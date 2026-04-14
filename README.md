# Binary And Red-Black Tree Project

A complete academic project that implements:

- Binary Search Trees (BST)
- Red-Black Trees (RBT)
- Word ingestion from RAE dictionary dataset
- Tree metrics and traversal reports
- Optional tree plotting with `matplotlib` + `networkx`

The repository includes both development code and a delivery-ready micro-repo prepared for assessment submission.

## Highlights

- Full BST implementation in `src/BinaryTree.py`
- Full RBT implementation (insert, delete, fixups, metrics, traversals) in `src/RedBlackTree.py`
- Interactive CLI project in `src/Proyecto.py`
- Plot generation utility in `src/plot_utils.py`
- Extended automated harness in `src/test.py`
- Delivery folder with isolated files in `Antonio_Urbano_Murillo_Proyecto/`

## Repository Structure

```text
BinaryAndRedBackTree/
  data/
    palabras_RAE_cleaned_noaccents.txt
  documentation/
    ProyectoBinaryAndRedBackTree.pdf
  src/
    BinaryTree.py
    RedBlackTree.py
    Proyecto.py
    plot_utils.py
    test.py
  Antonio_Urbano_Murillo_Proyecto/
    BinaryTree.py
    RedBlackTree.py
    Proyecto.py
    plot_utils.py
    tests_entrega.py
    data/
      palabras_RAE_cleaned_noaccents.txt
    plots/
```

## Requirements

- Python 3.10+
- pip

Optional plotting dependencies:

- `matplotlib`
- `networkx`

Install dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

Run test harness (development):

```bash
python src/test.py all
```

Run project CLI (development):

```bash
python src/Proyecto.py
```

Run test harness (delivery folder):

```bash
python Antonio_Urbano_Murillo_Proyecto/tests_entrega.py all
```

Run project CLI (delivery folder):

```bash
python Antonio_Urbano_Murillo_Proyecto/Proyecto.py
```

## CLI Flow (`Proyecto.py`)

The interactive CLI asks for:

1. Insertion mode:
   - `d`: default (file order)
   - `r`: random insertion
2. Tree type:
   - `b`: binary tree
   - `r`: red-black tree
3. Plot generation:
   - `s` / `n`
4. `HEIGHT` (integer > 0): number of layers used in generated plots
5. Up to 3 letters for filtering words from the dataset

## What Is Evaluated

For each selected letter, the project reports key metrics such as:

- root key
- root left and right child
- node count
- leaf count
- longest leaf-to-root path
- exact root-to-leaf paths with target edge length

For RBT mode, it also reports:

- tree height
- root skew status
- average depth

## Assessment Notes

This repository tracks two execution contexts:

- `src/`: ongoing development workspace
- `Antonio_Urbano_Murillo_Proyecto/`: delivery-ready micro-repo

The delivery folder contains self-contained paths for:

- dictionary data under `data/`
- generated plots under `plots/`
- independent test harness (`tests_entrega.py`)

## Code Style and Quality

- Type hints across key functions and methods
- Docstrings for core APIs
- `.editorconfig` for consistent formatting
- Non-destructive wrappers where compatibility was needed

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Acknowledgments

- Academic assignment specification in `documentation/ProyectoBinaryAndRedBackTree.pdf`
- Optional plotting stack: `matplotlib` and `networkx`
