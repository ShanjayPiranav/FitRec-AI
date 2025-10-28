from __future__ import annotations
from typing import Optional
import numpy as np
import joblib


class AdvancedQLearningAgent:
    def __init__(self, state_size: int = 11, num_actions: int = 5, alpha: float = 0.1, gamma: float = 0.95, epsilon: float = 0.1) -> None:
        self.state_size = state_size
        self.num_actions = num_actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table: dict = {}
        self.training_rewards: list[float] = []

    def _state_key(self, state: np.ndarray) -> tuple:
        return tuple(np.round(state, 2))

    def choose_action(self, state: np.ndarray) -> int:
        if np.random.rand() < self.epsilon:
            return int(np.random.randint(self.num_actions))
        key = self._state_key(state)
        if key not in self.q_table:
            self.q_table[key] = np.zeros(self.num_actions, dtype=np.float32)
        return int(np.argmax(self.q_table[key]))

    def learn(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray) -> None:
        s_key = self._state_key(state)
        ns_key = self._state_key(next_state)
        if s_key not in self.q_table:
            self.q_table[s_key] = np.zeros(self.num_actions, dtype=np.float32)
        if ns_key not in self.q_table:
            self.q_table[ns_key] = np.zeros(self.num_actions, dtype=np.float32)
        td_target = reward + self.gamma * float(np.max(self.q_table[ns_key]))
        td_error = td_target - float(self.q_table[s_key][action])
        self.q_table[s_key][action] += self.alpha * td_error

    def decay_epsilon(self, min_epsilon: float = 0.01, decay: float = 0.995) -> None:
        self.epsilon = max(min_epsilon, self.epsilon * decay)

    def save_model(self, path: Optional[str]) -> None:
        if not path:
            return
        joblib.dump({'q_table': self.q_table, 'meta': {'state_size': self.state_size, 'num_actions': self.num_actions}}, path)

    def load_model(self, path: Optional[str]) -> None:
        if not path:
            return
        try:
            data = joblib.load(path)
            self.q_table = data.get('q_table', {})
        except Exception:
            self.q_table = {}

    def get_action_confidence(self, state: np.ndarray, action: int) -> float:
        key = self._state_key(state)
        if key not in self.q_table:
            return 0.5
        q_vals = self.q_table[key]
        denom = float(np.max(np.abs(q_vals)) + 1e-6)
        return float(max(0.0, min(1.0, (q_vals[action] / denom) * 0.5 + 0.5)))
