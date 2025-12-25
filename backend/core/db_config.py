from __future__ import annotations

import json
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_CONFIG_FILE = BASE_DIR / "settings" / "db_config.json"

DEFAULT_CONFIG = {
    "host": "192.168.0.205",
    "port": 5432,
    "dbname": "report_system",
    "user": "postgres",
    "password": "rayyanshah04",
}


def load_db_config() -> dict[str, Any]:
    if DB_CONFIG_FILE.exists():
        with open(DB_CONFIG_FILE, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return {**DEFAULT_CONFIG, **(data or {})}
    return DEFAULT_CONFIG.copy()


def save_db_config(config: dict[str, Any]) -> dict[str, Any]:
    DB_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {**DEFAULT_CONFIG, **(config or {})}
    with open(DB_CONFIG_FILE, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)
    return payload
