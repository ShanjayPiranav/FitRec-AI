from __future__ import annotations
from typing import Any


def show_dashboard(summary: dict[str, Any]) -> None:
    print("=== DASHBOARD ===")
    for k, v in summary.items():
        print(f"{k}: {v}")
