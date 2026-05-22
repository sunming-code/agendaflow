"""Minimal LLM helpers for AgendaFlow."""

from __future__ import annotations

import time

from langchain_openai import ChatOpenAI
from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError

from config import config


RETRYABLE_EXCEPTIONS = (
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
)


def build_chat(
    *,
    api_key: str,
    base_url: str,
    model: str,
    temperature: float = 0.2,
    timeout: int | None = None,
) -> ChatOpenAI:
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        api_key=api_key,
        base_url=base_url,
        timeout=timeout or config.LLM_TIMEOUT_SECONDS,
        max_retries=2,
    )


def invoke_with_retry(chain, payload, label: str, max_retries: int = 3):
    for attempt in range(1, max_retries + 1):
        try:
            return chain.invoke(payload)
        except RETRYABLE_EXCEPTIONS as exc:
            if attempt >= max_retries:
                raise
            delay = 2 ** attempt if isinstance(exc, RateLimitError) else 2
            print(f"  {label} failed on attempt {attempt}: {type(exc).__name__}; retrying in {delay}s...")
            time.sleep(delay)
