from project.models import db, Workout, User
from datetime import datetime

def seed_workouts():
    """Seed the database with sample workouts"""
    workouts_data = [
        # Strength Training
        {
            'name': 'Push-ups',
            'category': 'strength',
            'muscle_group': 'chest, triceps, shoulders',
            'equipment': 'bodyweight',
            'difficulty': 'beginner',
            'duration': 10,
            'calories_burn': 50,
            'description': 'Classic bodyweight exercise for upper body strength',
            'instructions': 'Start in plank position, lower body until chest nearly touches ground, push back up'
        },
        {
            'name': 'Squats',
            'category': 'strength',
            'muscle_group': 'legs, glutes',
            'equipment': 'bodyweight',
            'difficulty': 'beginner',
            'duration': 15,
            'calories_burn': 80,
            'description': 'Fundamental lower body exercise',
            'instructions': 'Stand with feet shoulder-width apart, lower body as if sitting back, return to standing'
        },
        {
            'name': 'Deadlifts',
            'category': 'strength',
            'muscle_group': 'back, legs, core',
            'equipment': 'barbell',
            'difficulty': 'intermediate',
            'duration': 20,
            'calories_burn': 120,
            'description': 'Compound exercise for overall strength',
            'instructions': 'Stand with barbell on ground, bend at hips and knees, lift bar while keeping back straight'
        },
        {
            'name': 'Bench Press',
            'category': 'strength',
            'muscle_group': 'chest, triceps, shoulders',
            'equipment': 'barbell',
            'difficulty': 'intermediate',
            'duration': 25,
            'calories_burn': 150,
            'description': 'Classic chest exercise',
            'instructions': 'Lie on bench, lower barbell to chest, press back up to starting position'
        },
        {
            'name': 'Pull-ups',
            'category': 'strength',
            'muscle_group': 'back, biceps',
            'equipment': 'bodyweight',
            'difficulty': 'intermediate',
            'duration': 15,
            'calories_burn': 90,
            'description': 'Upper body pulling exercise',
            'instructions': 'Hang from pull-up bar, pull body up until chin over bar, lower back down'
        },
        
        # Cardio
        {
            'name': 'Running',
            'category': 'cardio',
            'muscle_group': 'legs, cardiovascular',
            'equipment': 'none',
            'difficulty': 'beginner',
            'duration': 30,
            'calories_burn': 300,
            'description': 'High-intensity cardiovascular exercise',
            'instructions': 'Start with a warm-up walk, gradually increase to running pace, maintain steady rhythm'
        },
        {
            'name': 'Cycling',
            'category': 'cardio',
            'muscle_group': 'legs, cardiovascular',
            'equipment': 'bicycle',
            'difficulty': 'beginner',
            'duration': 45,
            'calories_burn': 400,
            'description': 'Low-impact cardiovascular exercise',
            'instructions': 'Adjust seat height, maintain proper posture, pedal at consistent cadence'
        },
        {
            'name': 'Jump Rope',
            'category': 'cardio',
            'muscle_group': 'legs, cardiovascular, coordination',
            'equipment': 'jump rope',
            'difficulty': 'intermediate',
            'duration': 20,
            'calories_burn': 200,
            'description': 'High-intensity cardio with coordination benefits',
            'instructions': 'Hold rope handles, jump over rope as it passes under feet, maintain rhythm'
        },
        {
            'name': 'Swimming',
            'category': 'cardio',
            'muscle_group': 'full body, cardiovascular',
            'equipment': 'pool',
            'difficulty': 'intermediate',
            'duration': 40,
            'calories_burn': 350,
            'description': 'Full-body low-impact exercise',
            'instructions': 'Use proper stroke technique, maintain breathing rhythm, focus on form'
        },
        {
            'name': 'Rowing',
            'category': 'cardio',
            'muscle_group': 'full body, cardiovascular',
            'equipment': 'rowing machine',
            'difficulty': 'intermediate',
            'duration': 30,
            'calories_burn': 280,
            'description': 'Full-body cardio exercise',
            'instructions': 'Start with legs extended, pull handle to chest while leaning back, return to start'
        },
        
        # Flexibility
        {
            'name': 'Yoga',
            'category': 'flexibility',
            'muscle_group': 'full body',
            'equipment': 'yoga mat',
            'difficulty': 'beginner',
            'duration': 60,
            'calories_burn': 150,
            'description': 'Mind-body exercise for flexibility and relaxation',
            'instructions': 'Follow guided sequence, focus on breathing, hold poses with proper alignment'
        },
        {
            'name': 'Stretching',
            'category': 'flexibility',
            'muscle_group': 'full body',
            'equipment': 'none',
            'difficulty': 'beginner',
            'duration': 20,
            'calories_burn': 50,
            'description': 'Basic flexibility exercise',
            'instructions': 'Hold each stretch for 30 seconds, breathe deeply, don\'t bounce'
        },
        {
            'name': 'Pilates',
            'category': 'flexibility',
            'muscle_group': 'core, full body',
            'equipment': 'mat',
            'difficulty': 'intermediate',
            'duration': 45,
            'calories_burn': 180,
            'description': 'Core-focused flexibility and strength exercise',
            'instructions': 'Focus on core engagement, maintain proper form, control movements'
        },
        
        # Advanced Exercises
        {
            'name': 'Burpees',
            'category': 'strength',
            'muscle_group': 'full body',
            'equipment': 'bodyweight',
            'difficulty': 'advanced',
            'duration': 15,
            'calories_burn': 100,
            'description': 'High-intensity full-body exercise',
            'instructions': 'Start standing, drop to push-up position, perform push-up, jump back up'
        },
        {
            'name': 'Mountain Climbers',
            'category': 'cardio',
            'muscle_group': 'core, legs, cardiovascular',
            'equipment': 'bodyweight',
            'difficulty': 'intermediate',
            'duration': 10,
            'calories_burn': 80,
            'description': 'Dynamic cardio exercise',
            'instructions': 'Start in plank position, alternate bringing knees to chest rapidly'
        },
        {
            'name': 'Plank',
            'category': 'strength',
            'muscle_group': 'core',
            'equipment': 'bodyweight',
            'difficulty': 'beginner',
            'duration': 5,
            'calories_burn': 30,
            'description': 'Core stability exercise',
            'instructions': 'Hold body in straight line from head to heels, engage core muscles'
        }
    ]
    
    for workout_data in workouts_data:
        workout = Workout(**workout_data)
        db.session.add(workout)
    
    db.session.commit()
    print(f"Seeded {len(workouts_data)} workouts")

def seed_sample_users():
    """Seed the database with sample users"""
    users_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'age': 28,
            'gender': 'male',
            'weight': 75.0,
            'height': 180.0,
            'fitness_level': 'intermediate',
            'goals': 'muscle_gain, strength',
            'preferences': '{"equipment": ["barbell", "dumbbells"], "preferred_duration": 45, "time_of_day": "evening"}'
        },
        {
            'username': 'jane_smith',
            'email': 'jane@example.com',
            'age': 32,
            'gender': 'female',
            'weight': 60.0,
            'height': 165.0,
            'fitness_level': 'beginner',
            'goals': 'weight_loss, endurance',
            'preferences': '{"equipment": ["bodyweight", "cardio"], "preferred_duration": 30, "time_of_day": "morning"}'
        },
        {
            'username': 'mike_wilson',
            'email': 'mike@example.com',
            'age': 45,
            'gender': 'male',
            'weight': 85.0,
            'height': 175.0,
            'fitness_level': 'advanced',
            'goals': 'strength, muscle_gain',
            'preferences': '{"equipment": ["barbell", "dumbbells", "bodyweight"], "preferred_duration": 60, "time_of_day": "afternoon"}'
        },
        {
            'username': 'sarah_jones',
            'email': 'sarah@example.com',
            'age': 25,
            'gender': 'female',
            'weight': 55.0,
            'height': 160.0,
            'fitness_level': 'intermediate',
            'goals': 'flexibility, endurance',
            'preferences': '{"equipment": ["yoga mat", "bodyweight"], "preferred_duration": 45, "time_of_day": "evening"}'
        }
    ]
    
    for user_data in users_data:
        user = User(**user_data)
        db.session.add(user)
    
    db.session.commit()
    print(f"Seeded {len(users_data)} users")

def seed_sample_workout_history():
    """Seed the database with sample workout history"""
    from models import WorkoutHistory
    import random
    
    # Get all users and workouts
    users = User.query.all()
    workouts = Workout.query.all()
    
    if not users or not workouts:
        print("No users or workouts found. Please seed them first.")
        return
    
    # Create sample workout history
    for user in users:
        # Create 5-10 random workout history entries per user
        num_entries = random.randint(5, 10)
        
        for _ in range(num_entries):
            workout = random.choice(workouts)
            date = datetime.now() - timedelta(days=random.randint(1, 30))
            
            history = WorkoutHistory(
                user_id=user.id,
                workout_id=workout.id,
                date=date,
                duration=random.randint(workout.duration - 5, workout.duration + 10),
                intensity=random.randint(6, 10),
                enjoyment_rating=random.randint(3, 5),
                difficulty_rating=random.randint(2, 5),
                completion_rate=random.uniform(0.7, 1.0),
                notes=f"Sample workout session for {user.username}"
            )
            db.session.add(history)
    
    db.session.commit()
    print("Seeded sample workout history")

if __name__ == "__main__":
    from app import create_app
    from datetime import timedelta
    
    app = create_app()
    with app.app_context():
        seed_workouts()
        seed_sample_users()
        seed_sample_workout_history()
        print("Database seeding completed!")
