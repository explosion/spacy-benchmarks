from os import path
from pathlib import Path


HERE = Path(path.dirname(__file__))
DATA_DIR = HERE.parent / Path('data')
VENV_DIR = HERE.parent / Path('.env')
CACHE_DIR = HERE.parent / Path('cache')
GIGA_LOC = DATA_DIR / Path('gigaword.db')
