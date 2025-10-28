from __future__ import annotations
from typing import Dict, Any
from . import __init__  # noqa: F401
from ..core.rl_environment import HealthState


class EnhancedUserProfile:
    def __init__(self, username: str) -> None:
        self.username = username
        self.preferences: Dict[str, Any] = {'intensity_bias': 2}

    def get_current_health_state(self) -> HealthState:
        return HealthState()

    def get_preferences(self) -> Dict[str, Any]:
        return self.preferences

    def add_workout_session(self, session_data: Dict[str, Any], performance_score: float) -> None:
        return None

    def get_progress_analysis(self) -> Dict[str, Any]:
        return {'summary': 'stub'}

    def get_health_state_before_workout(self) -> HealthState:
        return HealthState()
