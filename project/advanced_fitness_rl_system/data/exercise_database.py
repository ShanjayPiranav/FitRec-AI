from __future__ import annotations
from typing import Dict, Any
from ..core.rl_environment import HealthState


class ComprehensiveExerciseDatabase:
    def __init__(self) -> None:
        self.actions = {
            0: {'exercise_name': 'Rest', 'intensity': 'none'},
            1: {'exercise_name': 'Squat', 'intensity': 'low'},
            2: {'exercise_name': 'Pushup', 'intensity': 'medium'},
            3: {'exercise_name': 'Burpees', 'intensity': 'high'},
            4: {'exercise_name': 'Rehab Mobility', 'intensity': 'low'},
        }

    def get_recommendation(self, action_index: int, health_state: HealthState, preferences: Dict[str, Any]) -> Dict[str, Any]:
        base = self.actions.get(action_index, self.actions[1]).copy()
        base['action_index'] = action_index
        base['duration'] = 60 if action_index == 0 else 120
        return base
