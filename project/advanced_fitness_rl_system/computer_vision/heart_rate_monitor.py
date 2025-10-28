from __future__ import annotations
from typing import Optional
import numpy as np


class HeartRateMonitor:
    def __init__(self, buffer_size: int = 150) -> None:
        self.buffer_size = buffer_size
        self.buffer: list[float] = []
        self.fps: float = 30.0

    def extract_heart_rate(self, frame: np.ndarray) -> Optional[float]:
        # Placeholder: return a plausible heart rate trend
        value = 100.0 + 5.0 * np.random.randn()
        self.buffer.append(float(value))
        if len(self.buffer) > self.buffer_size:
            self.buffer.pop(0)
        return float(max(55.0, min(185.0, value)))
