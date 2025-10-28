from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from project.models import db, User, Workout, WorkoutHistory


from project.rl_agent import WorkoutRecommendationAgent, EnhancedWorkoutRecommendationAgent

from datetime import datetime, timedelta
import json
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout_recommendations.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Initialize RL agents
    rl_agent = WorkoutRecommendationAgent()
    enhanced_agent = EnhancedWorkoutRecommendationAgent()
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            data = request.form
            
            # Check if user already exists
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                flash('User with this email already exists!', 'error')
                return render_template('register.html')
            
            # Create new user
            user = User(
                username=data['username'],
                email=data['email'],
                age=int(data['age']),
                gender=data['gender'],
                weight=float(data['weight']),
                height=float(data['height']),
                fitness_level=data['fitness_level'],
                goals=data['goals']
            )
            
            # Set default preferences
            default_preferences = {
                'equipment': [],
                'preferred_duration': 30,
                'time_of_day': 'morning'
            }
            user.set_preferences(default_preferences)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        
        return render_template('register.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            data = request.form
            user = User.query.filter_by(email=data['email']).first()
            
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'Welcome back, {user.username}!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email. Please try again.', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    def logout():
        session.clear()
        flash('You have been logged out.', 'info')
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # Get recent workout history
        recent_workouts = WorkoutHistory.query.filter_by(user_id=user.id)\
            .order_by(WorkoutHistory.date.desc()).limit(5).all()
        
        # Get user insights
        insights = rl_agent.get_user_insights(user)
        
        return render_template('dashboard.html', user=user, recent_workouts=recent_workouts, insights=insights)
    
    @app.route('/recommendations')
    def recommendations():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # Get all available workouts
        available_workouts = Workout.query.all()
        
        # Get personalized recommendations
        recommended_workouts = rl_agent.get_recommendations(user, available_workouts, num_recommendations=10)
        
        # Calculate diversity score
        diversity_score = rl_agent.get_workout_diversity(recommended_workouts)
        
        return render_template('recommendations.html', 
                             user=user, 
                             workouts=recommended_workouts,
                             diversity_score=diversity_score)
    
    @app.route('/workout/<int:workout_id>')
    def workout_detail(workout_id):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        workout = Workout.query.get_or_404(workout_id)
        user = User.query.get(session['user_id'])
        
        # Get user's history with this workout
        workout_history = WorkoutHistory.query.filter_by(
            user_id=user.id, 
            workout_id=workout_id
        ).order_by(WorkoutHistory.date.desc()).all()
        
        return render_template('workout_detail.html', 
                             workout=workout, 
                             user=user,
                             history=workout_history)
    
    @app.route('/complete_workout/<int:workout_id>', methods=['POST'])
    def complete_workout(workout_id):
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        data = request.json
        user = User.query.get(session['user_id'])
        workout = Workout.query.get_or_404(workout_id)
        
        # Create workout history entry
        history = WorkoutHistory(
            user_id=user.id,
            workout_id=workout_id,
            duration=data.get('duration', workout.duration),
            intensity=data.get('intensity', 7),
            enjoyment_rating=data.get('enjoyment_rating', 3),
            difficulty_rating=data.get('difficulty_rating', 3),
            completion_rate=data.get('completion_rate', 1.0),
            notes=data.get('notes', '')
        )
        
        db.session.add(history)
        db.session.commit()
        
        # Update RL model with feedback
        feedback = [
            data.get('enjoyment_rating', 3),
            data.get('difficulty_rating', 3),
            data.get('completion_rate', 1.0),
            data.get('intensity', 7)
        ]
        rl_agent.update_model(user.id, workout_id, feedback)
        
        return jsonify({'success': True, 'message': 'Workout completed successfully!'})
    
    @app.route('/profile', methods=['GET', 'POST'])
    def profile():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            data = request.form
            
            # Update user profile
            user.age = int(data['age'])
            user.weight = float(data['weight'])
            user.height = float(data['height'])
            user.fitness_level = data['fitness_level']
            user.goals = data['goals']
            
            # Update preferences
            preferences = user.get_preferences()
            preferences['equipment'] = request.form.getlist('equipment')
            preferences['preferred_duration'] = int(data['preferred_duration'])
            preferences['time_of_day'] = data['time_of_day']
            user.set_preferences(preferences)
            
            db.session.commit()
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
        
        return render_template('profile.html', user=user)
    
    @app.route('/history')
    def workout_history():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # Get all workout history
        history = WorkoutHistory.query.filter_by(user_id=user.id)\
            .order_by(WorkoutHistory.date.desc()).all()
        
        return render_template('history.html', user=user, history=history)
    
    @app.route('/analytics')
    def analytics():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        # Get user insights
        insights = rl_agent.get_user_insights(user)
        
        # Get workout history for charts
        history = WorkoutHistory.query.filter_by(user_id=user.id).all()
        
        # Prepare data for charts
        chart_data = {
            'categories': {},
            'difficulty': {},
            'enjoyment_trend': [],
            'completion_trend': []
        }
        
        for entry in history:
            workout = entry.workout
            
            # Category distribution
            if workout.category not in chart_data['categories']:
                chart_data['categories'][workout.category] = 0
            chart_data['categories'][workout.category] += 1
            
            # Difficulty distribution
            if workout.difficulty not in chart_data['difficulty']:
                chart_data['difficulty'][workout.difficulty] = 0
            chart_data['difficulty'][workout.difficulty] += 1
            
            # Trends over time
            chart_data['enjoyment_trend'].append({
                'date': entry.date.strftime('%Y-%m-%d'),
                'enjoyment': entry.enjoyment_rating
            })
            chart_data['completion_trend'].append({
                'date': entry.date.strftime('%Y-%m-%d'),
                'completion': entry.completion_rate
            })
        
        return render_template('analytics.html', 
                             user=user, 
                             insights=insights,
                             chart_data=chart_data)
    
    @app.route('/api/workouts')
    def api_workouts():
        """API endpoint to get all workouts"""
        workouts = Workout.query.all()
        return jsonify([{
            'id': w.id,
            'name': w.name,
            'category': w.category,
            'muscle_group': w.muscle_group,
            'equipment': w.equipment,
            'difficulty': w.difficulty,
            'duration': w.duration,
            'calories_burn': w.calories_burn,
            'description': w.description
        } for w in workouts])
    
    @app.route('/api/recommendations')
    def api_recommendations():
        """API endpoint to get personalized recommendations"""
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        available_workouts = Workout.query.all()
        recommended_workouts = rl_agent.get_recommendations(user, available_workouts, num_recommendations=5)
        
        return jsonify([{
            'id': w.id,
            'name': w.name,
            'category': w.category,
            'muscle_group': w.muscle_group,
            'equipment': w.equipment,
            'difficulty': w.difficulty,
            'duration': w.duration,
            'calories_burn': w.calories_burn,
            'description': w.description
        } for w in recommended_workouts])
    
    @app.route('/health-input', methods=['GET', 'POST'])
    def health_input():
        """Health input form for enhanced recommendations"""
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return redirect(url_for('login'))
        
        if request.method == 'POST':
            data = request.form
            
            # Get health inputs
            fatigue_level = int(data.get('fatigue_level', 5))
            days_since_last = int(data.get('days_since_last', 1))
            injury_constraints = data.get('injury_constraints', '').split(',') if data.get('injury_constraints') else []
            injury_constraints = [injury.strip() for injury in injury_constraints if injury.strip()]
            
            # Get enhanced recommendation
            recommendation = enhanced_agent.get_recommendation(
                user, 
                fatigue_level, 
                days_since_last, 
                injury_constraints
            )
            
            if 'error' in recommendation:
                flash(recommendation['error'], 'error')
                return render_template('health_input.html', user=user)
            
            # Store recommendation in session for completion
            session['current_recommendation'] = recommendation
            
            return render_template('enhanced_recommendation.html', 
                                 user=user, 
                                 recommendation=recommendation)
        
        return render_template('health_input.html', user=user)
    
    @app.route('/complete-enhanced-workout', methods=['POST'])
    def complete_enhanced_workout():
        """Complete enhanced workout with feedback"""
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        if 'current_recommendation' not in session:
            return jsonify({'error': 'No current recommendation'}), 400
        
        user = User.query.get(session['user_id'])
        if not user:
            session.clear()
            return jsonify({'error': 'User not found'}), 404
        
        data = request.form
        recommendation = session['current_recommendation']
        
        # Find the workout
        workout = Workout.query.filter_by(name=recommendation['workout_name']).first()
        if not workout:
            return jsonify({'error': 'Workout not found'}), 404
        
        # Create workout history entry
        history = WorkoutHistory(
            user_id=user.id,
            workout_id=workout.id,
            date=datetime.now(),
            actual_duration=int(data.get('actual_duration', recommendation['duration'])),
            intensity=data.get('intensity', 'medium'),
            enjoyment_rating=int(data.get('enjoyment_rating', 3)),
            difficulty_rating=int(data.get('difficulty_rating', 3)),
            completion_rate=float(data.get('completion_rate', 1.0)),
            notes=data.get('notes', '')
        )
        
        db.session.add(history)
        db.session.commit()
        
        # Update enhanced RL agent
        feedback = {
            'enjoyment': int(data.get('enjoyment_rating', 3)),
            'difficulty': int(data.get('difficulty_rating', 3)),
            'completion': float(data.get('completion_rate', 1.0))
        }
        
        state = recommendation['state']
        action = recommendation['intensity_level']
        
        enhanced_agent.update_from_feedback(user, state, action, feedback)
        
        # Clear session
        session.pop('current_recommendation', None)
        
        flash('Workout completed and feedback recorded! The AI has learned from your experience.', 'success')
        return redirect(url_for('dashboard'))
    
    @app.route('/api/health-progression')
    def api_health_progression():
        """API endpoint to get health progression data"""
        if 'user_id' not in session:
            return jsonify({'error': 'Not logged in'}), 401
        
        user = User.query.get(session['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        progression_data = enhanced_agent.get_health_progression_chart(user)
        return jsonify(progression_data)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
