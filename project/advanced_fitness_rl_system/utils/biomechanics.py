from __future__ import annotations
from typing import Tuple
import math


def calculate_joint_angle(a: Tuple[float, float], b: Tuple[float, float], c: Tuple[float, float]) -> float:
    ab = (a[0] - b[0], a[1] - b[1])
    cb = (c[0] - b[0], c[1] - b[1])
    dot = ab[0] * cb[0] + ab[1] * cb[1]
    mag_ab = math.hypot(ab[0], ab[1])
    mag_cb = math.hypot(cb[0], cb[1])
    if mag_ab == 0 or mag_cb == 0:
        return 180.0
    cos_theta = max(-1.0, min(1.0, dot / (mag_ab * mag_cb)))
    angle = math.degrees(math.acos(cos_theta))
    return float(angle)


def calculate_joint_distance(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return float(math.hypot(a[0] - b[0], a[1] - b[1]))
