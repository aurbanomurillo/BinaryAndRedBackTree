# Contributing

Thanks for your interest in improving this project.

## Development Setup

1. Use Python 3.10+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests before opening changes:

```bash
python src/test.py all
```

## Branch and Commit Guidelines

- Keep changes scoped and atomic.
- Use clear commit messages with intent + scope.
- Avoid mixing refactors and behavior changes when possible.

## Coding Guidelines

- Follow existing project style and naming.
- Preserve public interfaces unless explicitly requested.
- Add type hints and docstrings for new public methods.
- Prefer small, testable functions.

## Validation Checklist

Before submitting:

1. Ensure tests pass.
2. Ensure CLI flows still run:
   - `python src/Proyecto.py`
   - `python Antonio_Urbano_Murillo_Proyecto/Proyecto.py`
3. If plotting code changes, verify PNG generation still works.

## Delivery Folder

If your change affects submission files, mirror the required updates in:

- `Antonio_Urbano_Murillo_Proyecto/`

and re-run:

```bash
python Antonio_Urbano_Murillo_Proyecto/tests_entrega.py all
```
