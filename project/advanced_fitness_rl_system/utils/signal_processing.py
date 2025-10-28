from __future__ import annotations
from typing import Iterable, List


def moving_average(values: Iterable[float], window: int = 5) -> List[float]:
    buf: List[float] = []
    out: List[float] = []
    for v in values:
        buf.append(float(v))
        if len(buf) > window:
            buf.pop(0)
        out.append(sum(buf) / len(buf))
    return out
