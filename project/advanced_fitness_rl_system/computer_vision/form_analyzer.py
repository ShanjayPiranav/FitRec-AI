from typing import Dict


class FormAnalyzer:
    def __init__(self, templates_file: str | None = None) -> None:
        self.templates_file = templates_file

    def evaluate_form(self, pose_landmarks: Dict | None, exercise: str) -> float:
        return 65.0

    def assess_injury_risk(self, pose_landmarks: Dict | None, exercise: str) -> float:
        return 12.0
