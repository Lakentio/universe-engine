"""Simple module to manage game saves.

Usage:
- `save_state(name, state_dict)` -> creates a JSON file under `saves/` with a safe name and timestamp
- `list_saves()` -> returns a list of saves ordered by date (newest first)
- `load_state(name_or_filename)` -> loads a save by full filename or by name (chooses the most recent match)
- `delete_save(filename)` -> removes a save file

Saved data should contain at least: `cam_pos`, `cam_rot`, `selected_star` and `seed`.
"""
import os
import json
import time
import re
from typing import Dict, Any, List, Optional

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_SAVES_DIR = os.path.join(_ROOT_DIR, 'saves')

def _ensure_dir():
    if not os.path.exists(_SAVES_DIR):
        os.makedirs(_SAVES_DIR, exist_ok=True)

def _safe_name(name: str) -> str:
    # Remove unwanted characters
    safe = re.sub(r'[^0-9A-Za-z._-]', '_', name)
    return safe[:64]

def save_state(name: str, state: Dict[str, Any]) -> str:
    """Save the `state` dictionary under `name`. Returns the saved file path."""
    _ensure_dir()
    safe = _safe_name(name)
    ts = int(time.time())
    filename = f"{safe}_{ts}.json"
    path = os.path.join(_SAVES_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'meta': {'name': name, 'timestamp': ts}, 'state': state}, f, ensure_ascii=False, indent=2)
    return path

def list_saves() -> List[Dict[str, Any]]:
    """Return a list of saves with metadata ordered from newest to oldest."""
    _ensure_dir()
    items = []
    for fn in os.listdir(_SAVES_DIR):
        if not fn.endswith('.json'):
            continue
        fp = os.path.join(_SAVES_DIR, fn)
        try:
            with open(fp, 'r', encoding='utf-8') as f:
                data = json.load(f)
            meta = data.get('meta', {})
        except Exception:
            meta = {'name': fn}
        mtime = os.path.getmtime(fp)
        items.append({'filename': fn, 'path': fp, 'meta': meta, 'mtime': mtime})
    items.sort(key=lambda x: x['mtime'], reverse=True)
    return items

def load_state(name_or_filename: str) -> Optional[Dict[str, Any]]:
    """Load a save. If `name_or_filename` is an existing filename it will be used directly.
    Otherwise, try to find saves whose meta.name or filename contains the string and pick the most recent match."""
    _ensure_dir()
    # 1) if it is an exact path/filename
    candidate = None
    full_path = os.path.join(_SAVES_DIR, name_or_filename)
    if os.path.exists(full_path):
        candidate = full_path
    else:
        # search for similar saves in the list
        matches = []
        for s in list_saves():
            if name_or_filename in s['filename'] or name_or_filename in str(s.get('meta', {}).get('name', '')):
                matches.append(s)
        if matches:
            candidate = matches[0]['path']  # most recent

    if not candidate:
        return None

    try:
        with open(candidate, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('state') or {}
    except Exception:
        return None

def delete_save(filename: str) -> bool:
    _ensure_dir()
    path = os.path.join(_SAVES_DIR, filename)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False
