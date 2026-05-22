"""Result persistence for AgendaFlow runs."""

from __future__ import annotations

import json
import os
from datetime import datetime

from config import config


def save_result(result: dict) -> str:
    os.makedirs(config.RESULTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    protocol = str(result.get("protocol", "agendaflow"))
    path = os.path.join(config.RESULTS_DIR, f"{timestamp}_{protocol}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    return path
