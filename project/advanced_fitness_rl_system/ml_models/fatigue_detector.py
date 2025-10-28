from __future__ import annotations
from typing import List


class FatigueDetector:
    def detect(self, form_scores: List[float]) -> float:
        if not form_scores:
            return 0.0
        return max(0.0, min(1.0, (form_scores[0] - form_scores[-1]) / 100.0))
