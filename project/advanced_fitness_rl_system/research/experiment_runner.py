from __future__ import annotations
from typing import Callable, Any, Dict


def run_ab_test(variant_a: Callable[[], Dict[str, Any]], variant_b: Callable[[], Dict[str, Any]]) -> Dict[str, Any]:
    a = variant_a()
    b = variant_b()
    return {'A': a, 'B': b}
