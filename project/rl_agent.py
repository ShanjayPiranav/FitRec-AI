import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from project.models import Workout, WorkoutHistory, User
import json
import pickle
import os

class EnhancedWorkoutRecommendationAgent:
    """
    Enhanced Reinforcement Learning Agent for personalized workout recommendations
    Models the recommendation problem as an RL environment with health state inputs
    """
    
    def __init__(self, exploration_rate=0.1, learning_rate=0.01, discount_factor=0.95):
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        
        # Q-table: state -> action -> Q-value
        self.q_table = {}
        
        # State space components
        self.fitness_levels = list(range(1, 11))  # 1-10
        self.fatigue_levels = list(range(1, 11))  # 1-10
        self.days_since_last = ['0-1', '2-3', '4-7', '8+']
        self.age_groups = ['18-25', '26-35', '36-45', '46-55', '55+']
        self.injury_flags = [True, False]
        
        # Action space: workout intensity levels
        self.intensity_levels = ['low', 'medium', 'high']
        
        # Exercise database by intensity and muscle groups
        self.exercise_database = self._initialize_exercise_database()
        
        # User profiles and Q-tables persistence
        self.user_profiles = {}
        self.q_table_file = 'q_table.pkl'
        self.profiles_file = 'user_profiles.pkl'
        
        # Load existing data
        self._load_persisted_data()
    
    def _initialize_exercise_database(self) -> Dict:
        """Initialize exercise database categorized by intensity, muscle groups, and injury suitability"""
        return {
            'low': {
                'cardio': ['Walking', 'Light Cycling', 'Swimming', 'Yoga'],
                'strength': ['Bodyweight Squats', 'Wall Push-ups', 'Light Dumbbell Curls'],
                'flexibility': ['Stretching', 'Tai Chi', 'Pilates']
            },
            'medium': {
                'cardio': ['Jogging', 'Cycling', 'Rowing', 'Elliptical'],
                'strength': ['Push-ups', 'Squats', 'Lunges', 'Dumbbell Rows'],
                'flexibility': ['Dynamic Stretching', 'Yoga Flow', 'Mobility Work']
            },
            'high': {
                'cardio': ['Running', 'HIIT', 'Sprinting', 'Boxing'],
                'strength': ['Deadlifts', 'Bench Press', 'Pull-ups', 'Weighted Squats'],
                'flexibility': ['Advanced Yoga', 'Gymnastics', 'Contortion']
            }
        }
    
    def get_user_health_state(self, user: User, fatigue_level: int, days_since_last: int, 
                             injury_constraints: List[str] = None) -> Tuple:
        """
        Create state tuple from user health inputs
        State: (fitness, fatigue, days_since_last, age_group, injury_flag)
        """
        # Fitness level (1-10)
        fitness_level = self._encode_fitness_level(user.fitness_level)
        
        # Fatigue level (1-10)
        fatigue_level = max(1, min(10, fatigue_level))
        
        # Days since last workout
        if days_since_last <= 1:
            days_category = '0-1'
        elif days_since_last <= 3:
            days_category = '2-3'
        elif days_since_last <= 7:
            days_category = '4-7'
        else:
            days_category = '8+'
        
        # Age group
        age_group = self._get_age_group(user.age)
        
        # Injury flag
        injury_flag = bool(injury_constraints and len(injury_constraints) > 0)
        
        return (fitness_level, fatigue_level, days_category, age_group, injury_flag)
    
    def _encode_fitness_level(self, level: str) -> int:
        """Encode fitness level as numerical feature (1-10)"""
        encoding = {
            'beginner': 3,
            'intermediate': 6,
            'advanced': 9
        }
        return encoding.get(level, 5)
    
    def _get_age_group(self, age: int) -> str:
        """Categorize user by age group"""
        if age < 26:
            return '18-25'
        elif age < 36:
            return '26-35'
        elif age < 46:
            return '36-45'
        elif age < 56:
            return '46-55'
        else:
            return '55+'
    
    def get_available_actions(self, state: Tuple, injury_constraints: List[str] = None) -> List[str]:
        """Get available intensity levels based on current state and injury constraints"""
        fitness_level, fatigue_level, days_since_last, age_group, injury_flag = state
        
        available_intensities = []
        
        # Base intensity based on fitness and fatigue
        if fitness_level >= 7 and fatigue_level <= 3:
            available_intensities.append('high')
        if fitness_level >= 4 and fatigue_level <= 6:
            available_intensities.append('medium')
        if fitness_level >= 1:
            available_intensities.append('low')
        
        # Adjust for injury constraints
        if injury_flag:
            # Remove high intensity if injuries present
            if 'high' in available_intensities:
                available_intensities.remove('high')
            # Add specific injury considerations
            if injury_constraints:
                if 'back' in injury_constraints:
                    # Avoid exercises that strain back
                    pass
                if 'knee' in injury_constraints:
                    # Prefer low-impact exercises
                    if 'high' in available_intensities:
                        available_intensities.remove('high')
        
        # Ensure at least one option is available
        if not available_intensities:
            available_intensities = ['low']
        
        return available_intensities
    
    def select_action(self, state: Tuple, available_workouts: List[Workout], 
                     injury_constraints: List[str] = None) -> Tuple[str, Workout]:
        """
        Select action using ε-greedy policy
        Returns: (intensity_level, specific_workout)
        """
        available_actions = self.get_available_actions(state, injury_constraints)
        
        # ε-greedy exploration
        if np.random.random() < self.exploration_rate:
            # Exploration: random action
            intensity = np.random.choice(available_actions)
        else:
            # Exploitation: best action based on Q-values
            intensity = self._get_best_action(state, available_actions)
        
        # Select specific workout for the chosen intensity
        workout = self._select_workout_for_intensity(intensity, available_workouts, injury_constraints)
        
        return intensity, workout
    
    def _get_best_action(self, state: Tuple, available_actions: List[str]) -> str:
        """Get best action based on Q-values"""
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.intensity_levels}
        
        q_values = self.q_table[state]
        best_action = available_actions[0]
        best_value = q_values.get(best_action, 0.0)
        
        for action in available_actions:
            value = q_values.get(action, 0.0)
            if value > best_value:
                best_value = value
                best_action = action
        
        return best_action
    
    def _select_workout_for_intensity(self, intensity: str, available_workouts: List[Workout], 
                                    injury_constraints: List[str] = None) -> Workout:
        """Select specific workout for given intensity level"""
        # Filter workouts by intensity
        intensity_workouts = []
        for workout in available_workouts:
            workout_intensity = self._get_workout_intensity(workout)
            if workout_intensity == intensity:
                # Check injury constraints
                if not injury_constraints or self._is_workout_safe(workout, injury_constraints):
                    intensity_workouts.append(workout)
        
        if not intensity_workouts:
            # Fallback to any available workout
            return available_workouts[0] if available_workouts else None
        
        # Select based on user preferences and history
        return self._select_best_workout(intensity_workouts)
    
    def _get_workout_intensity(self, workout: Workout) -> str:
        """Determine workout intensity level"""
        # Map workout difficulty to intensity
        if workout.difficulty == 'beginner':
            return 'low'
        elif workout.difficulty == 'intermediate':
            return 'medium'
        else:
            return 'high'
    
    def _is_workout_safe(self, workout: Workout, injury_constraints: List[str]) -> bool:
        """Check if workout is safe for given injury constraints"""
        if not injury_constraints:
            return True
        
        # Simple safety checks (can be expanded)
        workout_name = workout.name.lower()
        for injury in injury_constraints:
            if injury.lower() == 'back' and any(word in workout_name for word in ['deadlift', 'bend', 'twist']):
                return False
            if injury.lower() == 'knee' and any(word in workout_name for word in ['jump', 'squat', 'lunge']):
                return False
        
        return True
    
    def _select_best_workout(self, workouts: List[Workout]) -> Workout:
        """Select best workout from available options"""
        # Simple selection - can be enhanced with more sophisticated logic
        return workouts[0]
    
    def calculate_reward(self, state: Tuple, action: str, user_feedback: Dict) -> float:
        """
        Calculate reward based on user feedback and health outcomes
        Positive for fitness improvement and user comfort, negative for overexertion or injury risk
        """
        fitness_level, fatigue_level, days_since_last, age_group, injury_flag = state
        
        # Base reward from user feedback
        enjoyment = user_feedback.get('enjoyment', 3) / 5.0  # Normalize to 0-1
        difficulty = user_feedback.get('difficulty', 3) / 5.0
        completion = user_feedback.get('completion', 0.8)
        
        # Calculate reward components
        reward = 0.0
        
        # Enjoyment component
        reward += enjoyment * 0.4
        
        # Completion component
        reward += completion * 0.3
        
        # Difficulty appropriateness
        if action == 'low' and difficulty <= 0.4:
            reward += 0.2  # Good match
        elif action == 'medium' and 0.3 <= difficulty <= 0.7:
            reward += 0.2  # Good match
        elif action == 'high' and difficulty >= 0.6:
            reward += 0.2  # Good match
        else:
            reward -= 0.1  # Poor match
        
        # Fatigue management
        if fatigue_level > 7 and action == 'high':
            reward -= 0.3  # Penalty for high intensity when fatigued
        
        # Recovery consideration
        if days_since_last == '0-1' and action == 'high':
            reward -= 0.2  # Penalty for high intensity on consecutive days
        
        # Injury risk
        if injury_flag and action == 'high':
            reward -= 0.4  # Penalty for high intensity with injuries
        
        return reward
    
    def update_q_value(self, state: Tuple, action: str, reward: float, next_state: Tuple = None):
        """
        Update Q-value using Q-learning update rule
        Q(s,a) = Q(s,a) + α[r + γ * max Q(s',a') - Q(s,a)]
        """
        if state not in self.q_table:
            self.q_table[state] = {action: 0.0 for action in self.intensity_levels}
        
        current_q = self.q_table[state].get(action, 0.0)
        
        # Calculate max Q-value for next state
        max_next_q = 0.0
        if next_state and next_state in self.q_table:
            max_next_q = max(self.q_table[next_state].values())
        
        # Q-learning update
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[state][action] = new_q
    
    def get_recommendation(self, user: User, fatigue_level: int, days_since_last: int,
                          injury_constraints: List[str] = None) -> Dict:
        """
        Get personalized workout recommendation based on current health state
        """
        # Get current state
        state = self.get_user_health_state(user, fatigue_level, days_since_last, injury_constraints)
        
        # Get available workouts
        available_workouts = Workout.query.all()
        
        # Select action
        intensity, workout = self.select_action(state, available_workouts, injury_constraints)
        
        if not workout:
            return {"error": "No suitable workout found"}
        
        # Create recommendation
        recommendation = {
            'workout_name': workout.name,
            'intensity_level': intensity,
            'duration': workout.duration,
            'category': workout.category,
            'muscle_group': workout.muscle_group,
            'equipment': workout.equipment,
            'description': workout.description,
            'instructions': workout.instructions,
            'state': state,
            'reasoning': self._get_recommendation_reasoning(state, intensity, workout)
        }
        
        return recommendation
    
    def _get_recommendation_reasoning(self, state: Tuple, intensity: str, workout: Workout) -> str:
        """Generate reasoning for the recommendation"""
        fitness_level, fatigue_level, days_since_last, age_group, injury_flag = state
        
        reasoning = f"Based on your fitness level ({fitness_level}/10), "
        
        if fatigue_level > 7:
            reasoning += f"fatigue level ({fatigue_level}/10), and "
        else:
            reasoning += f"energy level ({11-fatigue_level}/10), and "
        
        reasoning += f"{days_since_last} days since your last workout, "
        
        if injury_flag:
            reasoning += "considering your injury constraints, "
        
        reasoning += f"I recommend a {intensity} intensity workout: {workout.name}. "
        reasoning += f"This {workout.category} exercise targets {workout.muscle_group} "
        reasoning += f"and should take approximately {workout.duration} minutes."
        
        return reasoning
    
    def update_from_feedback(self, user: User, state: Tuple, action: str, 
                           user_feedback: Dict, next_state: Tuple = None):
        """
        Update Q-values based on user feedback after workout completion
        """
        # Calculate reward
        reward = self.calculate_reward(state, action, user_feedback)
        
        # Update Q-value
        self.update_q_value(state, action, reward, next_state)
        
        # Persist updated Q-table
        self._save_q_table()
    
    def _save_q_table(self):
        """Save Q-table to disk"""
        try:
            with open(self.q_table_file, 'wb') as f:
                pickle.dump(self.q_table, f)
        except Exception as e:
            print(f"Error saving Q-table: {e}")
    
    def _load_persisted_data(self):
        """Load Q-table and user profiles from disk"""
        try:
            if os.path.exists(self.q_table_file):
                with open(self.q_table_file, 'rb') as f:
                    self.q_table = pickle.load(f)
        except Exception as e:
            print(f"Error loading Q-table: {e}")
            self.q_table = {}
    
    def get_health_progression_chart(self, user: User) -> Dict:
        """Generate health progression chart data"""
        user_history = WorkoutHistory.query.filter_by(user_id=user.id).order_by(WorkoutHistory.date).all()
        
        if not user_history:
            return {"message": "No workout history available"}
        
        # Extract progression data
        dates = [h.date.strftime('%Y-%m-%d') for h in user_history]
        enjoyment_scores = [h.enjoyment_rating for h in user_history]
        difficulty_scores = [h.difficulty_rating for h in user_history]
        completion_rates = [h.completion_rate for h in user_history]
        
        return {
            'dates': dates,
            'enjoyment_scores': enjoyment_scores,
            'difficulty_scores': difficulty_scores,
            'completion_rates': completion_rates,
            'total_workouts': len(user_history)
        }

# Keep the original agent for backward compatibility
class WorkoutRecommendationAgent:
    """
    Reinforcement Learning Agent for personalized workout recommendations
    Uses Multi-Armed Bandit approach with contextual features
    """
    
    def __init__(self, exploration_rate=0.1, learning_rate=0.01):
        self.exploration_rate = exploration_rate
        self.learning_rate = learning_rate
        self.workout_arms = {}  # Store Q-values for each workout
        self.user_contexts = {}  # Store user-specific context
        self.feature_weights = {
            'enjoyment': 0.4,
            'difficulty': 0.2,
            'completion': 0.3,
            'intensity': 0.1
        }
    
    def get_user_context(self, user: User) -> Dict:
        """Extract user context features for personalization"""
        context = {
            'fitness_level': self._encode_fitness_level(user.fitness_level),
            'age_group': self._get_age_group(user.age),
            'goals': self._encode_goals(user.goals),
            'preferences': user.get_preferences()
        }
        return context
    
    def _encode_fitness_level(self, level: str) -> int:
        """Encode fitness level as numerical feature"""
        encoding = {'beginner': 1, 'intermediate': 2, 'advanced': 3}
        return encoding.get(level, 1)
    
    def _get_age_group(self, age: int) -> str:
        """Categorize user by age group"""
        if age < 25:
            return 'young'
        elif age < 45:
            return 'adult'
        else:
            return 'senior'
    
    def _encode_goals(self, goals: str) -> List[int]:
        """Encode fitness goals as binary features"""
        goal_list = goals.lower().split(',') if goals else []
        goal_encoding = {
            'weight_loss': [1, 0, 0, 0],
            'muscle_gain': [0, 1, 0, 0],
            'endurance': [0, 0, 1, 0],
            'flexibility': [0, 0, 0, 1]
        }
        
        encoded = [0, 0, 0, 0]
        for goal in goal_list:
            goal = goal.strip()
            if goal in goal_encoding:
                encoded = [max(a, b) for a, b in zip(encoded, goal_encoding[goal])]
        return encoded
    
    def get_workout_features(self, workout: Workout) -> Dict:
        """Extract features from workout"""
        return {
            'category': workout.category,
            'muscle_group': workout.muscle_group,
            'equipment': workout.equipment,
            'difficulty': self._encode_fitness_level(workout.difficulty),
            'duration': workout.duration,
            'calories_burn': workout.calories_burn
        }
    
    def calculate_similarity(self, workout1: Workout, workout2: Workout) -> float:
        """Calculate similarity between two workouts"""
        features1 = self.get_workout_features(workout1)
        features2 = self.get_workout_features(workout2)
        
        similarity = 0.0
        if features1['category'] == features2['category']:
            similarity += 0.3
        if features1['muscle_group'] == features2['muscle_group']:
            similarity += 0.3
        if features1['equipment'] == features2['equipment']:
            similarity += 0.2
        if features1['difficulty'] == features2['difficulty']:
            similarity += 0.2
            
        return similarity
    
    def get_recommendations(self, user: User, available_workouts: List[Workout], 
                          num_recommendations: int = 5) -> List[Workout]:
        """
        Get personalized workout recommendations using RL
        """
        user_context = self.get_user_context(user)
        user_id = user.id
        
        # Initialize user context if not exists
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = user_context
        
        # Get user's workout history
        user_history = WorkoutHistory.query.filter_by(user_id=user_id).all()
        
        # Calculate Q-values for each workout
        workout_scores = []
        
        for workout in available_workouts:
            # Base Q-value from historical performance
            q_value = self._calculate_q_value(workout, user_history)
            
            # Contextual bonus based on user preferences
            contextual_bonus = self._calculate_contextual_bonus(workout, user_context)
            
            # Exploration bonus
            exploration_bonus = self._get_exploration_bonus(workout, user_history)
            
            total_score = q_value + contextual_bonus + exploration_bonus
            workout_scores.append((workout, total_score))
        
        # Sort by score and return top recommendations
        workout_scores.sort(key=lambda x: x[1], reverse=True)
        return [workout for workout, _ in workout_scores[:num_recommendations]]
    
    def _calculate_q_value(self, workout: Workout, user_history: List[WorkoutHistory]) -> float:
        """Calculate Q-value based on historical performance"""
        workout_history = [h for h in user_history if h.workout_id == workout.id]
        
        if not workout_history:
            return 0.0  # No history, neutral score
        
        # Calculate average feedback score
        total_score = 0.0
        for history in workout_history:
            feedback = history.get_feedback_vector()
            weighted_score = sum(f * w for f, w in zip(feedback, self.feature_weights.values()))
            total_score += weighted_score
        
        return total_score / len(workout_history)
    
    def _calculate_contextual_bonus(self, workout: Workout, user_context: Dict) -> float:
        """Calculate bonus based on user context and preferences"""
        bonus = 0.0
        
        # Fitness level matching
        if workout.difficulty == user_context['fitness_level']:
            bonus += 0.2
        
        # Goal alignment
        goals = user_context['goals']
        if 'weight_loss' in goals and workout.category == 'cardio':
            bonus += 0.3
        elif 'muscle_gain' in goals and workout.category == 'strength':
            bonus += 0.3
        elif 'endurance' in goals and workout.category == 'cardio':
            bonus += 0.3
        
        # Equipment preference
        preferences = user_context['preferences']
        preferred_equipment = preferences.get('equipment', [])
        if workout.equipment in preferred_equipment:
            bonus += 0.1
        
        return bonus
    
    def _get_exploration_bonus(self, workout: Workout, user_history: List[WorkoutHistory]) -> float:
        """Calculate exploration bonus to encourage trying new workouts"""
        workout_tried = any(h.workout_id == workout.id for h in user_history)
        
        if not workout_tried:
            return self.exploration_rate
        return 0.0
    
    def update_model(self, user_id: int, workout_id: int, feedback: List[float]):
        """
        Update the RL model based on user feedback
        """
        # Update Q-value for the specific workout
        if workout_id not in self.workout_arms:
            self.workout_arms[workout_id] = 0.0
        
        # Calculate reward from feedback, handling None values
        reward = sum((f or 0) * w for f, w in zip(feedback, self.feature_weights.values()))
        
        # Update Q-value using Q-learning update rule
        current_q = self.workout_arms[workout_id]
        new_q = current_q + self.learning_rate * (reward - current_q)
        self.workout_arms[workout_id] = new_q
    
    def get_workout_diversity(self, recommendations: List[Workout]) -> float:
        """Calculate diversity of recommended workouts"""
        if len(recommendations) < 2:
            return 0.0
        
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(recommendations)):
            for j in range(i + 1, len(recommendations)):
                similarity = self.calculate_similarity(recommendations[i], recommendations[j])
                total_similarity += similarity
                comparisons += 1
        
        if comparisons == 0:
            return 0.0
        
        average_similarity = total_similarity / comparisons
        return 1.0 - average_similarity  # Higher diversity = lower similarity
    
    def get_user_insights(self, user: User) -> Dict:
        """Get insights about user's workout preferences"""
        user_history = WorkoutHistory.query.filter_by(user_id=user.id).all()
        
        if not user_history:
            return {"message": "No workout history available"}
        
        # Analyze preferences
        category_preferences = {}
        difficulty_preferences = {}
        enjoyment_scores = {}
        
        for history in user_history:
            workout = history.workout
            feedback = history.get_feedback_vector()
            
            # Category preferences
            if workout.category not in category_preferences:
                category_preferences[workout.category] = []
            category_preferences[workout.category].append(feedback[0])  # enjoyment
            
            # Difficulty preferences
            if workout.difficulty not in difficulty_preferences:
                difficulty_preferences[workout.difficulty] = []
            difficulty_preferences[workout.difficulty].append(feedback[1])  # difficulty rating
            
            # Overall enjoyment
            enjoyment_scores[workout.name] = feedback[0]
        
        # Calculate averages
        insights = {
            'favorite_categories': {cat: np.mean(scores) for cat, scores in category_preferences.items()},
            'preferred_difficulty': {diff: np.mean(scores) for diff, scores in difficulty_preferences.items()},
            'top_enjoyed_workouts': sorted(enjoyment_scores.items(), key=lambda x: x[1], reverse=True)[:5],
            'total_workouts': len(user_history),
            'average_enjoyment': np.mean([h.get_feedback_vector()[0] for h in user_history if h.get_feedback_vector()[0] > 0])
        }
        
        return insights
