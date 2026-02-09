import json
from pathlib import Path

DEFAULT_SEARCH_LIMIT = 5

def find_project_root(marker_files=(".git", " pyproject.toml")) -> Path:
    path = Path(__file__).resolve()
    for parent in [path] + list(path.parents):
        if any((parent / marker).exists() for marker in marker_files):
            return parent
    raise RuntimeError("Project root not found")

PROJECT_ROOT = find_project_root()
MOVIES_PATH = PROJECT_ROOT / "data" / "movies.json"
STOPWORDS_PATH = PROJECT_ROOT / "data" / "stopwords.txt"

def load_movies() -> list[dict]:
    with MOVIES_PATH.open() as f:
        data = json.load(f)
    return data["movies"]

def load_stopwords() -> list[str]:
    with STOPWORDS_PATH.open() as f:
        return f.read().splitlines()
    
