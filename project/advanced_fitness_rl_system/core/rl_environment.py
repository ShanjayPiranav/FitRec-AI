from dataclasses import dataclass
from typing import Tuple, Dict, Any
import time
import numpy as np
from ..computer_vision.pose_estimator import PoseEstimator
from ..computer_vision.form_analyzer import FormAnalyzer
from ..computer_vision.injury_predictor import InjuryPredictor
from ..computer_vision.heart_rate_monitor import HeartRateMonitor
from .reward_calculator import RewardCalculator


@dataclass
class HealthState:
    fitness_level: float = 5.0
    fatigue_level: float = 2.0
    recovery_score: float = 70.0
    heart_rate: int = 90
    form_quality_avg: float = 60.0
    injury_risk_score: float = 10.0
    days_since_workout: int = 1
    current_streak: int = 2
    preferred_intensity: int = 2


class AdvancedFitnessEnvironment:
    def __init__(self, use_camera: bool = False, camera_id: int = 0) -> None:
        self.use_camera = use_camera
        self.camera_id = camera_id
        self.current_health: HealthState = HealthState()
        # CV components (stubs safe when no camera)
        self.pose_estimator = PoseEstimator()
        self.form_analyzer = FormAnalyzer()
        self.injury_predictor = InjuryPredictor()
        self.hr_monitor = HeartRateMonitor()
        # Reward calculator
        self.reward_calc = RewardCalculator()
        # Session state
        self._episode_start_ts: float = time.time()
        self._weekly_load: float = 0.5

    def reset(self, user_health: HealthState) -> np.ndarray:
        self.current_health = user_health
        self._episode_start_ts = time.time()
        return self._get_state_vector()

    def _get_state_vector(self) -> np.ndarray:
        s = np.array([
            self.current_health.fitness_level / 10.0,
            self.current_health.fatigue_level / 10.0,
            self.current_health.recovery_score / 100.0,
            min(self.current_health.heart_rate, 200) / 200.0,
            self.current_health.form_quality_avg / 100.0,
            self.current_health.injury_risk_score / 100.0,
            min(self.current_health.days_since_workout, 14) / 14.0,
            min(self.current_health.current_streak, 30) / 30.0,
            self.current_health.preferred_intensity / 3.0,
            self._get_time_of_day_feature(),
            self._get_weekly_load_feature(),
        ], dtype=np.float32)
        return s

    def step(self, action: int, exercise_duration: int = 300) -> Tuple[np.ndarray, float, bool, Dict[str, Any]]:
        exercise_name = self._action_to_exercise(action)
        adapted_action = self._adapt_difficulty(action, self.current_health.form_quality_avg)

        # Simulated CV metrics (safe without camera)
        form_score, injury_risk, heart_rate = self._simulate_cv_execution(adapted_action, exercise_duration)

        # Compute reward using calculator
        base = [0, 10, 20, 30, 15][max(0, min(adapted_action, 4))]
        progressive_bonus = self._calculate_progressive_overload_bonus(adapted_action)
        reward = self.reward_calc.compute(
            base_reward=base,
            form_score=form_score,
            injury_risk=injury_risk,
            fatigue_level=self.current_health.fatigue_level,
            recovery_score=self.current_health.recovery_score,
            progressive_bonus=progressive_bonus,
        )

        next_state = self._get_state_vector()
        info = {
            'form_score': form_score,
            'injury_risk': injury_risk,
            'heart_rate': int(heart_rate),
            'exercise_completed': adapted_action > 0,
            'fatigue_increase': max(0.0, 0.3 * adapted_action),
            'exercise': exercise_name,
        }
        # Update proxy health state
        self._update_health_state_from_execution(form_score, injury_risk, int(heart_rate), adapted_action)
        done = False
        return next_state, float(reward), done, info

    # Helpers
    def _get_time_of_day_feature(self) -> float:
        hour = int(time.localtime().tm_hour)
        return float(hour) / 24.0

    def _get_weekly_load_feature(self) -> float:
        return float(self._weekly_load)

    def _action_to_exercise(self, action: int) -> str:
        mapping = {0: 'Rest', 1: 'Squat', 2: 'Pushup', 3: 'Burpees', 4: 'Rehab Mobility'}
        return mapping.get(int(action), 'Squat')

    def _adapt_difficulty(self, action: int, avg_form: float) -> int:
        if action <= 0:
            return 0
        if avg_form > 75.0:
            return min(4, action + 1)
        if avg_form < 45.0:
            return max(1, action - 1)
        return int(action)

    def _calculate_progressive_overload_bonus(self, action: int) -> float:
        return float(1.0 if action >= 2 else 0.2)

    def _simulate_cv_execution(self, action: int, duration: int) -> Tuple[float, float, int]:
        base_form = 60.0 + 5.0 * (action - 1)
        form_score = float(max(0.0, min(100.0, base_form + np.random.randn() * 3.0)))
        injury_risk = float(max(0.0, min(100.0, 10.0 + 5.0 * (action - 2) + np.random.randn() * 2.0)))
        heart_rate = int(max(55, min(190, 90 + 12 * action + np.random.randn() * 3.0)))
        return form_score, injury_risk, heart_rate

    def _update_health_state_from_execution(self, form_score: float, injury_risk: float, heart_rate: int, action: int) -> None:
        self.current_health.form_quality_avg = float(0.8 * self.current_health.form_quality_avg + 0.2 * form_score)
        self.current_health.injury_risk_score = float(0.7 * self.current_health.injury_risk_score + 0.3 * injury_risk)
        self.current_health.heart_rate = int(heart_rate)
        self.current_health.fatigue_level = float(min(10.0, self.current_health.fatigue_level + 0.2 * action))
        self._weekly_load = float(min(1.0, max(0.0, self._weekly_load + 0.02 * action - 0.01)))
