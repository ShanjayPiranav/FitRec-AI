from __future__ import annotations
from typing import Dict


class InjuryPredictor:
    def assess(self, pose_landmarks: Dict | None, exercise: str) -> float:
        if pose_landmarks is None:
            return 10.0
        return 15.0
