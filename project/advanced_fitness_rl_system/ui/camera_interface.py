from __future__ import annotations
from typing import Callable, Optional, Dict, Any
import numpy as np


class CameraInterface:
    def __init__(self, camera_id: int = 0) -> None:
        self.camera_id = camera_id
        self.window_name = "Fitness AI Monitor"
        self.current_exercise = "unknown"

    def start_monitoring(self, exercise: str, duration: int = 60, feedback_callback: Optional[Callable[[Dict[str, Any]], None]] = None) -> Dict[str, Any]:
        self.current_exercise = exercise
        form_scores: list[float] = []
        injury_risks: list[float] = []
        heart_rates: list[float] = []

        # Simulate frames
        total_frames = int(duration * 10)
        for i in range(total_frames):
            form = 60.0 + 10.0 * np.sin(i / 15.0)
            risk = 10.0 + 5.0 * np.cos(i / 20.0)
            hr = 100.0 + 15.0 * np.sin(i / 25.0)
            form_scores.append(float(form))
            injury_risks.append(float(max(0.0, risk)))
            heart_rates.append(float(max(50.0, hr)))
            if feedback_callback and i % 10 == 0:
                feedback_callback({'form_score': form_scores[-1], 'injury_risk': injury_risks[-1], 'heart_rate': heart_rates[-1], 'time': i / 10.0})

        return {
            'duration': float(duration),
            'average_form_score': float(np.mean(form_scores)) if form_scores else 0.0,
            'average_heart_rate': float(np.mean(heart_rates)) if heart_rates else 0.0,
            'max_injury_risk': float(np.max(injury_risks)) if injury_risks else 0.0,
            'total_frames': total_frames,
            'exercise': exercise,
        }
