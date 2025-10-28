from __future__ import annotations
from typing import Dict


class FormClassifier:
    def predict(self, pose_landmarks: Dict | None, exercise: str) -> float:
        return 0.5
