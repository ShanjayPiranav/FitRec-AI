from __future__ import annotations
from typing import Dict


class RewardCalculator:
    def __init__(self, weights: Dict[str, float] | None = None) -> None:
        self.weights = weights or {
            'base': 1.0,
            'form_bonus': 1.0,
            'injury_penalty': 1.0,
            'fatigue_penalty': 1.0,
            'recovery_bonus': 1.0,
            'progressive_bonus': 1.0,
        }

    def compute(self, base_reward: float, form_score: float, injury_risk: float, fatigue_level: float, recovery_score: float, progressive_bonus: float) -> float:
        form_modifier = (form_score - 50.0) / 10.0
        injury_penalty = -injury_risk / 5.0
        fatigue_penalty = -fatigue_level * 2.0
        recovery_bonus = recovery_score / 10.0
        total = (
            self.weights['base'] * base_reward
            + self.weights['form_bonus'] * form_modifier
            + self.weights['injury_penalty'] * injury_penalty
            + self.weights['fatigue_penalty'] * fatigue_penalty
            + self.weights['recovery_bonus'] * recovery_bonus
            + self.weights.get('progressive_bonus', 1.0) * progressive_bonus
        )
        return float(total)
