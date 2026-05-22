"""Interactive entrypoint for lightweight AgendaFlow."""

from __future__ import annotations

import sys

from AGENDAFLOW import run_agendaflow
from config import config


def _input_with_default(prompt: str, default: str = "", *, secret: bool = False) -> str:
    suffix = f" [{default}]" if default and not secret else ""
    print(f"{prompt}{suffix}: ", end="", flush=True)
    value = sys.stdin.readline()
    if value == "":
        return default
    value = value.rstrip("\r\n").strip()
    return value or default


def _input_role_count(default: int = 4) -> int:
    raw = _input_with_default("Role count (2-8, optional)", str(default))
    try:
        value = int(raw)
    except ValueError:
        value = default
    return max(2, min(8, value))


def _input_task() -> str:
    print("\nEnter your problem/task. Finish with an empty line:")
    lines: list[str] = []
    while True:
        line = sys.stdin.readline()
        if line == "":
            break
        line = line.rstrip("\r\n")
        if not line and lines:
            break
        if line:
            lines.append(line)
    return "\n".join(lines).strip()


def main():
    print("AgendaFlow lightweight runner")
    print("-" * 32)
    api_key = _input_with_default("API key", config.OPENAI_API_KEY, secret=True)
    base_url = _input_with_default("API base URL", config.OPENAI_API_BASE)
    model = _input_with_default("Model name", config.MODEL_NAME)
    role_count = _input_role_count(4)
    task = _input_task()

    if not api_key:
        print("API key is required.")
        return
    if not base_url:
        print("API base URL is required.")
        return
    if not model:
        print("Model name is required.")
        return
    if not task:
        print("Task cannot be empty.")
        return

    try:
        result = run_agendaflow(
            task=task,
            api_key=api_key,
            base_url=base_url,
            model=model,
            role_count=role_count,
        )
    except Exception as exc:
        print(f"\nAgendaFlow failed: {exc}")
        raise

    print("\n" + "=" * 60)
    print("Final Answer")
    print("=" * 60)
    print(result.final_answer)
    print(f"\nSaved result: {result.saved_path}")


if __name__ == "__main__":
    main()
