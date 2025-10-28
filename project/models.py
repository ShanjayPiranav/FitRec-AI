from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model to store user profiles and preferences"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    weight = db.Column(db.Float)  # in kg
    height = db.Column(db.Float)  # in cm
    fitness_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    goals = db.Column(db.String(200))  # weight_loss, muscle_gain, endurance, etc.
    preferences = db.Column(db.Text)  # JSON string of user preferences
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    workout_history = db.relationship('WorkoutHistory', backref='user', lazy=True)
    
    def get_preferences(self):
        """Get user preferences as a dictionary"""
        if self.preferences:
            return json.loads(self.preferences)
        return {}
    
    def set_preferences(self, preferences_dict):
        """Set user preferences from a dictionary"""
        self.preferences = json.dumps(preferences_dict)

class Workout(db.Model):
    """Workout/exercise model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # strength, cardio, flexibility, etc.
    muscle_group = db.Column(db.String(100))  # chest, back, legs, etc.
    equipment = db.Column(db.String(100))  # dumbbells, barbell, bodyweight, etc.
    difficulty = db.Column(db.String(20))  # beginner, intermediate, advanced
    duration = db.Column(db.Integer)  # estimated duration in minutes
    calories_burn = db.Column(db.Integer)  # estimated calories burned
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    
    # Relationships
    workout_history = db.relationship('WorkoutHistory', backref='workout', lazy=True)

class WorkoutHistory(db.Model):
    """Model to track user workout history and feedback"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)  # actual duration in minutes
    intensity = db.Column(db.Integer)  # 1-10 scale
    enjoyment_rating = db.Column(db.Integer)  # 1-5 scale
    difficulty_rating = db.Column(db.Integer)  # 1-5 scale
    completion_rate = db.Column(db.Float)  # 0-1 scale
    notes = db.Column(db.Text)
    
    def get_feedback_vector(self):
        """Get feedback as a vector for RL algorithm"""
        return [
            self.enjoyment_rating if self.enjoyment_rating is not None else 0,
            self.difficulty_rating if self.difficulty_rating is not None else 0,
            self.completion_rate if self.completion_rate is not None else 0,
            self.intensity if self.intensity is not None else 0
        ]
