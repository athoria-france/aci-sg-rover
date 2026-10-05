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
uv run rover.py input.txt
```

Exemple de fichier d'entrée :

```
5 5
1 2 N
LMLMLMLMM
3 3 E
MMRMMRMRRM
```

Sortie (stdout) :

```
1 3 N
5 1 E
```

### Format d'entrée

- Ligne 1 : coin supérieur droit du Plateau (`x y`, entiers positifs ou nuls).
- Puis, pour chaque Rover, deux lignes : sa position initiale (`x y H`, `H` : la direction parmi `N E S W`)
  et ses Instructions (`L`, `R`, `M`, éventuellement aucune).
- Fins de ligne `\n`, `\r\n` ou `\r` ou autres séparateurs de ligne Unicode (`\v`, `\f`, ...), comme défini par splitlines.
- Casse ignorée, valeurs séparées par exactement un espace, aucun espace en début ou fin de ligne.
- Aucune ligne vide n'est acceptée, sauf comme ligne d'Instructions (Rover sans Instruction).

### Règles de la Mission

- Tous les Rovers sont posés au départ, dans l'ordre du fichier, puis explorent l'un après l'autre.
- Un Rover dont la position initiale est hors du Plateau ou sur une case occupée n'est pas posé.
- Un déplacement vers l'extérieur du Plateau ou vers un autre Rover est ignoré, le Rover continue.
- Ces incidents sont signalés sur stderr, par exemple :
  `[WARN] Rover #2 - Move blocked (6 6 N): outside plateau`.

### Codes de sortie

| Code | Signification |
|------|---------------|
| 0 | Mission explorée (même avec des incidents) |
| 1 | Mission rejetée : fichier illisible ou mal formé (`[ERROR] Line 3 - invalid heading 'X'`), aucune sortie sur stdout |
| 2 | Mauvais usage de la ligne de commande |

## Architecture

Architecture hexagonale, modélisation DDD. Les dépendances pointent vers le domaine : `adapters` dépend
de `application`, qui dépend de `domain`, qui ne dépend de rien.

- `src/domain/` : le modèle métier, exprimé dans le langage ubiquitaire. Il porte les règles de la
  Mission et garantit ses invariants, sans aucune dépendance technique (fichiers, flux, format texte).
- `src/application/` : les cas d'usage, qui orchestrent le domaine, et les ports, qui définissent ce
  que l'application attend du monde extérieur et ce qu'elle lui offre.
- `src/adapters/` : la traduction entre le monde extérieur et l'application. Ils implémentent les ports
  et portent tous les détails techniques : ligne de commande, format du fichier d'entrée, écriture sur
  stdout et stderr.
- `src/main.py` : la racine de composition, seul endroit où les adapters sont instanciés et reliés aux
  cas d'usage.