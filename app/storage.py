from typing import Any

LAST_SUNO_CALLBACK: dict[str, Any] | None = None
SUNO_CALLBACK_HISTORY: list[dict[str, Any]] = []
SUNO_TASK_INDEX: dict[str, list[dict[str, Any]]] = {}