# sg-rover

## Installation

```bash
uv sync
```

## Qualité de code

```bash
uv run ruff check .              # lint
uv run ruff format .             # formatage
uv run mypy                      # typage (strict)
uv run bandit -c pyproject.toml -r rover.py src   # sécurité (code)
uv run pytest                    # tests + couverture (min. 80 %)
```

Audit des dépendances (sécurité), à partir de `uv.lock` :

```bash
uv export --no-emit-project --format requirements-txt -o requirements-audit.txt
uv run pip-audit --disable-pip -r requirements-audit.txt
```

## Lancer l'application

```bash
uv run rover.py
```