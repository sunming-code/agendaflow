"""Runtime configuration for the lightweight AgendaFlow runner."""

from __future__ import annotations

import os


class Config:
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    OPENAI_API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.moonshot.cn/v1")
    MODEL_NAME = os.environ.get("MODEL_NAME", "kimi-k2-turbo-preview")
    LLM_TIMEOUT_SECONDS = int(os.environ.get("LLM_TIMEOUT_SECONDS", "60"))

    RESULTS_DIR = os.environ.get(
        "AGENDAFLOW_RESULTS_DIR",
        os.path.join(PROJECT_DIR, "agendaflow_results"),
    )


config = Config()
