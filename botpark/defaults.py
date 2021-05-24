from pathlib import Path

import appdirs


CACHE_DIR = Path(appdirs.user_cache_dir('botpark', 'fishsouprecipe'))
CACHE_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE = CACHE_DIR / 'state.json'
