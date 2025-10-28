from __future__ import annotations

USE_CAMERA: bool = False
CAMERA_ID: int = 0
FRAME_WIDTH: int = 1280
FRAME_HEIGHT: int = 720
DEFAULT_SESSION_DURATION: int = 120
STATE_SIZE: int = 11
NUM_ACTIONS: int = 5

# Reward weights
REWARD_WEIGHTS = {
    'base': 1.0,
    'form_bonus': 1.0,
    'injury_penalty': 1.0,
    'fatigue_penalty': 1.0,
    'recovery_bonus': 1.0,
}
