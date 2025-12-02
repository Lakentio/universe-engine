"""Módulo simples para gerenciar saves do jogo.

Forma de uso:
- `save_state(name, state_dict)` -> cria um arquivo JSON em `saves/` com nome seguro e timestamp
- `list_saves()` -> retorna lista de saves ordenada por data (mais recente primeiro)
- `load_state(name_or_filename)` -> carrega um save pelo filename completo ou pelo nome (pega o mais recente que combine)
- `delete_save(filename)` -> remove um save

Os saves armazenam pelo menos: `cam_pos`, `cam_rot`, `selected_star` e `seed`.
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
    # Remove caracteres indesejados
    safe = re.sub(r'[^0-9A-Za-z._-]', '_', name)
    return safe[:64]

def save_state(name: str, state: Dict[str, Any]) -> str:
    """Salva o dicionário `state` com o `name`. Retorna o caminho do arquivo salvo."""
    _ensure_dir()
    safe = _safe_name(name)
    ts = int(time.time())
    filename = f"{safe}_{ts}.json"
    path = os.path.join(_SAVES_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'meta': {'name': name, 'timestamp': ts}, 'state': state}, f, ensure_ascii=False, indent=2)
    return path

def list_saves() -> List[Dict[str, Any]]:
    """Retorna lista de saves com metadados ordenados do mais recente ao mais antigo."""
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
    """Carrega um save. Se `name_or_filename` for um filename existente é usado diretamente.
    Caso contrário, tenta encontrar saves cujo meta.name ou filename contenha a string e escolhe o mais recente."""
    _ensure_dir()
    # 1) se for caminho/filename exato
    candidate = None
    full_path = os.path.join(_SAVES_DIR, name_or_filename)
    if os.path.exists(full_path):
        candidate = full_path
    else:
        # busca por similaridade na lista de saves
        matches = []
        for s in list_saves():
            if name_or_filename in s['filename'] or name_or_filename in str(s.get('meta', {}).get('name', '')):
                matches.append(s)
        if matches:
            candidate = matches[0]['path']  # mais recente

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
