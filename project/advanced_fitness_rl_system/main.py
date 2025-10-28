import argparse
from typing import Dict, Any

from .core.rl_environment import AdvancedFitnessEnvironment, HealthState
from .core.q_learning_agent import AdvancedQLearningAgent
from .data.user_profile import EnhancedUserProfile
from .data.exercise_database import ComprehensiveExerciseDatabase
from .ui.camera_interface import CameraInterface
from .research.data_collector import ResearchDataCollector
from .utils.visualization import AdvancedVisualization


class AdvancedFitnessSystem:
    def __init__(self, username: str, use_camera: bool = True) -> None:
        self.username = username
        self.use_camera = use_camera
        self.env = AdvancedFitnessEnvironment(use_camera=use_camera)
        self.agent = AdvancedQLearningAgent()
        self.user_profile = EnhancedUserProfile(username)
        self.exercise_db = ComprehensiveExerciseDatabase()
        self.camera_interface = CameraInterface() if use_camera else None
        self.data_collector = ResearchDataCollector()
        self.visualizer = AdvancedVisualization()

    def get_ai_recommendation(self) -> Dict[str, Any]:
        health_state = self.user_profile.get_current_health_state()
        state_vector = self.env.reset(health_state)
        self.agent.epsilon = 0
        action = self.agent.choose_action(state_vector)
        recommendation = self.exercise_db.get_recommendation(action, health_state, self.user_profile.get_preferences())
        recommendation['ai_confidence'] = self.agent.get_action_confidence(state_vector, action)
        recommendation['explanation'] = f"Selected based on user state and preferences."
        return recommendation

    def execute_workout_with_monitoring(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        if not self.use_camera:
            _, reward, _, info = self.env.step(recommendation['action_index'])
            return {
                'session_data': {
                    'duration': recommendation['duration'],
                    'average_form_score': info.get('form_score', 50.0),
                    'average_heart_rate': info.get('heart_rate', 100),
                    'max_injury_risk': info.get('injury_risk', 10.0),
                    'total_frames': 0,
                    'exercise': recommendation['exercise_name'],
                },
                'performance_score': float(max(0.0, min(100.0, 50.0 + reward))),
            }
        summary = self.camera_interface.start_monitoring(exercise=recommendation['exercise_name'], duration=recommendation['duration'])
        return {'session_data': summary, 'performance_score': float(max(0.0, min(100.0, summary.get('average_form_score', 50.0))))}

    def train_agent(self, episodes: int = 100) -> None:
        for _ in range(episodes):
            hs = self.user_profile.get_current_health_state()
            s = self.env.reset(hs)
            a = self.agent.choose_action(s)
            ns, r, _, _ = self.env.step(a)
            self.agent.learn(s, a, r, ns)
        self.agent.save_model(None)


def main() -> None:
    parser = argparse.ArgumentParser(description='Advanced AI Fitness System (minimal)')
    parser.add_argument('--username', type=str, default='user')
    parser.add_argument('--train', type=int, default=0)
    parser.add_argument('--no-camera', action='store_true')
    args = parser.parse_args()

    system = AdvancedFitnessSystem(username=args.username, use_camera=not args.no_camera)

    if args.train > 0:
        system.train_agent(args.train)

    rec = system.get_ai_recommendation()
    print(f"Recommendation: {rec['exercise_name']} ({rec['intensity']}) for {rec['duration']}s | conf={rec['ai_confidence']:.2f}")
    results = system.execute_workout_with_monitoring(rec)
    print(f"Done. Performance ~ {results['performance_score']:.1f}. Avg form {results['session_data']['average_form_score']:.1f}%")


if __name__ == '__main__':
    main()
