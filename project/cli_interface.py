#!/usr/bin/env python3
"""
FitRec AI - CLI Interface
Command Line Interface for the Enhanced Workout Recommendation System
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User, Workout, WorkoutHistory
from rl_agent import EnhancedWorkoutRecommendationAgent

class FitRecCLI:
    """Command Line Interface for FitRec AI"""
    
    def __init__(self):
        self.app = create_app()
        self.agent = EnhancedWorkoutRecommendationAgent()
        self.current_user = None
        
    def run(self):
        """Main CLI loop"""
        print("🏋️  FitRec AI - Workout Recommendation System")
        print("=" * 50)
        
        while True:
            if not self.current_user:
                self._handle_authentication()
            else:
                self._show_main_menu()
    
    def _handle_authentication(self):
        """Handle user authentication"""
        print("\n🔐 Authentication")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == '1':
            self._login()
        elif choice == '2':
            self._register()
        elif choice == '3':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please try again.")
    
    def _login(self):
        """Handle user login"""
        print("\n📧 Login")
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        
        with self.app.app_context():
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                self.current_user = user
                print(f"✅ Welcome back, {user.username}!")
            else:
                print("❌ Invalid email or password.")
    
    def _register(self):
        """Handle user registration"""
        print("\n📝 Registration")
        
        username = input("Username: ").strip()
        email = input("Email: ").strip()
        password = input("Password: ").strip()
        age = int(input("Age: ").strip())
        weight = float(input("Weight (kg): ").strip())
        height = float(input("Height (cm): ").strip())
        
        print("\nFitness Level:")
        print("1. Beginner")
        print("2. Intermediate")
        print("3. Advanced")
        fitness_choice = input("Enter choice (1-3): ").strip()
        fitness_levels = ['beginner', 'intermediate', 'advanced']
        fitness_level = fitness_levels[int(fitness_choice) - 1]
        
        goals = input("Goals (comma-separated): ").strip()
        
        with self.app.app_context():
            user = User(
                username=username,
                email=email,
                age=age,
                weight=weight,
                height=height,
                fitness_level=fitness_level,
                goals=goals
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            self.current_user = user
            print(f"✅ Registration successful! Welcome, {username}!")
    
    def _show_main_menu(self):
        """Show main menu options"""
        print(f"\n👤 Welcome, {self.current_user.username}!")
        print("\n📋 Main Menu")
        print("1. Input Health Conditions & Get Recommendation")
        print("2. Rate Previous Workout")
        print("3. View Workout History")
        print("4. View Health Progression Charts")
        print("5. View User Profile")
        print("6. Logout")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            self._get_workout_recommendation()
        elif choice == '2':
            self._rate_workout()
        elif choice == '3':
            self._view_history()
        elif choice == '4':
            self._view_progression_charts()
        elif choice == '5':
            self._view_profile()
        elif choice == '6':
            self.current_user = None
            print("✅ Logged out successfully.")
        elif choice == '7':
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please try again.")
    
    def _get_workout_recommendation(self):
        """Get workout recommendation based on health inputs"""
        print("\n🏥 Health Input Form")
        print("Please provide your current health status:")
        
        # Fitness level (1-10)
        while True:
            try:
                fitness_level = int(input("Fitness Level (1-10): ").strip())
                if 1 <= fitness_level <= 10:
                    break
                else:
                    print("❌ Please enter a number between 1 and 10.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Fatigue level (1-10)
        while True:
            try:
                fatigue_level = int(input("Fatigue Level (1-10): ").strip())
                if 1 <= fatigue_level <= 10:
                    break
                else:
                    print("❌ Please enter a number between 1 and 10.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Days since last workout
        while True:
            try:
                days_since_last = int(input("Days since last workout: ").strip())
                if days_since_last >= 0:
                    break
                else:
                    print("❌ Please enter a non-negative number.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        # Injury constraints
        print("\nInjury Constraints (press Enter if none):")
        injury_input = input("Enter injuries (comma-separated, e.g., 'back,knee'): ").strip()
        injury_constraints = [injury.strip() for injury in injury_input.split(',') if injury.strip()] if injury_input else []
        
        # Equipment constraints
        print("\nEquipment Constraints (press Enter if none):")
        equipment_input = input("Enter available equipment (comma-separated, e.g., 'dumbbells,mat'): ").strip()
        equipment_constraints = [equipment.strip() for equipment in equipment_input.split(',') if equipment.strip()] if equipment_input else []
        
        with self.app.app_context():
            # Get recommendation
            recommendation = self.agent.get_recommendation(
                self.current_user, 
                fatigue_level, 
                days_since_last, 
                injury_constraints
            )
            
            if 'error' in recommendation:
                print(f"❌ {recommendation['error']}")
                return
            
            # Display recommendation
            print("\n" + "="*60)
            print("🎯 PERSONALIZED WORKOUT RECOMMENDATION")
            print("="*60)
            print(f"Workout: {recommendation['workout_name']}")
            print(f"Intensity: {recommendation['intensity_level'].upper()}")
            print(f"Category: {recommendation['category']}")
            print(f"Muscle Group: {recommendation['muscle_group']}")
            print(f"Duration: {recommendation['duration']} minutes")
            print(f"Equipment: {recommendation['equipment']}")
            print(f"\nDescription: {recommendation['description']}")
            print(f"\nInstructions: {recommendation['instructions']}")
            print(f"\n🤖 AI Reasoning: {recommendation['reasoning']}")
            print("="*60)
            
            # Store recommendation for rating
            self._current_recommendation = recommendation
    
    def _rate_workout(self):
        """Rate a completed workout"""
        print("\n⭐ Rate Your Workout")
        
        with self.app.app_context():
            # Get user's recent workouts
            recent_workouts = WorkoutHistory.query.filter_by(user_id=self.current_user.id)\
                .order_by(WorkoutHistory.date.desc()).limit(5).all()
            
            if not recent_workouts:
                print("❌ No recent workouts found to rate.")
                return
            
            print("\nRecent workouts:")
            for i, history in enumerate(recent_workouts, 1):
                print(f"{i}. {history.workout.name} ({history.date.strftime('%Y-%m-%d')})")
            
            try:
                choice = int(input("\nSelect workout to rate (1-5): ").strip())
                if 1 <= choice <= len(recent_workouts):
                    selected_history = recent_workouts[choice - 1]
                else:
                    print("❌ Invalid choice.")
                    return
            except ValueError:
                print("❌ Please enter a valid number.")
                return
            
            # Get ratings
            print(f"\nRating workout: {selected_history.workout.name}")
            
            while True:
                try:
                    enjoyment = int(input("Enjoyment Rating (1-5): ").strip())
                    if 1 <= enjoyment <= 5:
                        break
                    else:
                        print("❌ Please enter a number between 1 and 5.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            while True:
                try:
                    difficulty = int(input("Difficulty Rating (1-5): ").strip())
                    if 1 <= difficulty <= 5:
                        break
                    else:
                        print("❌ Please enter a number between 1 and 5.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            while True:
                try:
                    completion = float(input("Completion Rate (0.0-1.0): ").strip())
                    if 0.0 <= completion <= 1.0:
                        break
                    else:
                        print("❌ Please enter a number between 0.0 and 1.0.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            
            # Update workout history
            selected_history.enjoyment_rating = enjoyment
            selected_history.difficulty_rating = difficulty
            selected_history.completion_rate = completion
            db.session.commit()
            
            # Update RL agent
            feedback = {
                'enjoyment': enjoyment,
                'difficulty': difficulty,
                'completion': completion
            }
            
            # Get current state (simplified)
            state = self.agent.get_user_health_state(
                self.current_user, 
                fatigue_level=5,  # Default value
                days_since_last=1,  # Default value
                injury_constraints=[]
            )
            
            action = self.agent._get_workout_intensity(selected_history.workout)
            
            self.agent.update_from_feedback(
                self.current_user,
                state,
                action,
                feedback
            )
            
            print("✅ Workout rated successfully! The AI has learned from your feedback.")
    
    def _view_history(self):
        """View workout history"""
        print("\n📊 Workout History")
        
        with self.app.app_context():
            history = WorkoutHistory.query.filter_by(user_id=self.current_user.id)\
                .order_by(WorkoutHistory.date.desc()).all()
            
            if not history:
                print("❌ No workout history found.")
                return
            
            print(f"\nTotal workouts: {len(history)}")
            print("\nRecent workouts:")
            print("-" * 80)
            print(f"{'Date':<12} {'Workout':<20} {'Category':<12} {'Duration':<10} {'Enjoyment':<10} {'Difficulty':<10}")
            print("-" * 80)
            
            for entry in history[:10]:  # Show last 10 workouts
                print(f"{entry.date.strftime('%Y-%m-%d'):<12} "
                      f"{entry.workout.name:<20} "
                      f"{entry.workout.category:<12} "
                      f"{entry.actual_duration:<10} "
                      f"{entry.enjoyment_rating:<10} "
                      f"{entry.difficulty_rating:<10}")
    
    def _view_progression_charts(self):
        """View health progression charts"""
        print("\n📈 Health Progression Charts")
        
        with self.app.app_context():
            chart_data = self.agent.get_health_progression_chart(self.current_user)
            
            if 'message' in chart_data:
                print(f"❌ {chart_data['message']}")
                return
            
            print(f"\nTotal workouts tracked: {chart_data['total_workouts']}")
            
            if chart_data['dates']:
                print("\nRecent progression:")
                print("-" * 60)
                print(f"{'Date':<12} {'Enjoyment':<10} {'Difficulty':<10} {'Completion':<10}")
                print("-" * 60)
                
                # Show last 10 entries
                for i in range(min(10, len(chart_data['dates']))):
                    date = chart_data['dates'][-(i+1)]
                    enjoyment = chart_data['enjoyment_scores'][-(i+1)]
                    difficulty = chart_data['difficulty_scores'][-(i+1)]
                    completion = chart_data['completion_rates'][-(i+1)]
                    
                    print(f"{date:<12} {enjoyment:<10} {difficulty:<10} {completion:<10.2f}")
            
            # Calculate trends
            if len(chart_data['enjoyment_scores']) >= 5:
                recent_enjoyment = sum(chart_data['enjoyment_scores'][-5:]) / 5
                earlier_enjoyment = sum(chart_data['enjoyment_scores'][-10:-5]) / 5
                
                if recent_enjoyment > earlier_enjoyment:
                    trend = "📈 Improving"
                elif recent_enjoyment < earlier_enjoyment:
                    trend = "📉 Declining"
                else:
                    trend = "➡️ Stable"
                
                print(f"\nTrend: {trend}")
    
    def _view_profile(self):
        """View user profile"""
        print("\n👤 User Profile")
        print("-" * 40)
        print(f"Username: {self.current_user.username}")
        print(f"Email: {self.current_user.email}")
        print(f"Age: {self.current_user.age}")
        print(f"Weight: {self.current_user.weight} kg")
        print(f"Height: {self.current_user.height} cm")
        print(f"Fitness Level: {self.current_user.fitness_level}")
        print(f"Goals: {self.current_user.goals}")
        
        # Calculate BMI
        height_m = self.current_user.height / 100
        bmi = self.current_user.weight / (height_m ** 2)
        print(f"BMI: {bmi:.1f}")
        
        # BMI category
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 25:
            category = "Normal weight"
        elif bmi < 30:
            category = "Overweight"
        else:
            category = "Obese"
        print(f"BMI Category: {category}")

def main():
    """Main function to run the CLI"""
    try:
        cli = FitRecCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
