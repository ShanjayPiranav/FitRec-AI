# FitRec AI - Personalized Workout Recommendation System

A comprehensive AI-powered workout recommendation system using reinforcement learning to provide personalized fitness suggestions based on user preferences, performance history, and feedback.

## 🚀 Features

### 🤖 AI-Powered Recommendations
- **Enhanced RL Environment**: Models recommendation problem as proper RL environment with state, actions, and rewards
- **Health State Modeling**: Considers fitness level (1-10), fatigue level (1-10), days since last workout, age, weight, and injury constraints
- **Q-Learning Agent**: Implements ε-greedy policy to learn optimal workout intensity and exercise types
- **Reward System**: Positive rewards for fitness improvement and user comfort, negative for overexertion or injury risk
- **Continuous Learning**: Improves recommendations over time based on user feedback (1-5 ratings)
- **Exploration vs Exploitation**: Balances trying new workouts with proven favorites

### 👤 User Management
- **Comprehensive Profiles**: Age, gender, weight, height, fitness level, and goals
- **Health Input System**: Real-time health status input including fatigue, injury constraints, and equipment availability
- **Preference Tracking**: Equipment preferences, preferred duration, and time of day
- **Progress Monitoring**: Track workout completion, enjoyment, and performance metrics
- **CLI Interface**: Command-line interface for advanced users and automation

### 📊 Analytics & Insights
- **Performance Analytics**: Detailed charts and statistics
- **AI-Generated Insights**: Personalized recommendations and patterns
- **Progress Tracking**: Visual representation of fitness journey
- **Trend Analysis**: Enjoyment and completion rate trends over time

### 🏋️ Workout Management
- **Diverse Workout Library**: 15+ workout types across strength, cardio, and flexibility
- **Exercise Database**: Categorized by intensity, muscle groups, and injury suitability
- **Detailed Workout Information**: Instructions, muscle groups, equipment needed
- **Interactive Feedback System**: Rate enjoyment, difficulty, and completion
- **Workout History**: Complete tracking of all completed workouts
- **Health Progression Charts**: Visual tracking of fitness improvement over time

### 🎨 Modern UI/UX
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Modern Interface**: Clean, intuitive design with Bootstrap 5
- **Interactive Elements**: Real-time feedback and dynamic content
- **Visual Analytics**: Charts and graphs for data visualization

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **AI/ML**: Custom reinforcement learning algorithm
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for cloning the repository)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd workout-recommendation-system
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
python data_seeder.py
```

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Application
Open your browser and navigate to: `http://localhost:5000`

## 🎯 Quick Start Guide

### 1. Create an Account
- Visit the registration page
- Fill in your basic information and fitness profile
- Set your fitness goals and preferences

### 2. Get Recommendations
- Log in to your account
- Navigate to the "Recommendations" page
- View AI-generated workout suggestions tailored to your profile

### 3. Complete Workouts
- Click on any recommended workout
- Follow the instructions and complete the workout
- Provide feedback on enjoyment, difficulty, and completion

### 4. Enhanced Health Input (New!)
- Use the "Health Input" feature for advanced recommendations
- Input current fitness level, fatigue, days since last workout
- Specify injury constraints and available equipment
- Get AI reasoning for personalized workout selection

### 5. CLI Interface (New!)
- Run `python cli_interface.py` for command-line access
- Input health conditions and get recommendations
- Rate workouts and view progression charts
- Perfect for automation and advanced users

### 6. Track Progress
- Visit the "Analytics" page to view detailed insights
- Check your workout history and performance trends
- Monitor your progress over time

## 📊 Demo Accounts

For testing purposes, the following demo accounts are available:

- **Beginner User**: `jane@example.com`
- **Advanced User**: `mike@example.com`

## 🏗️ Project Structure

```
workout-recommendation-system/
├── app.py                 # Main Flask application
├── models.py             # Database models and relationships
├── rl_agent.py           # Reinforcement learning algorithm
├── cli_interface.py      # Command-line interface
├── data_seeder.py        # Database seeding script
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── index.html       # Landing page
│   ├── register.html    # User registration
│   ├── login.html       # User login
│   ├── dashboard.html   # User dashboard
│   ├── recommendations.html  # Workout recommendations
│   ├── health_input.html     # Health input form
│   ├── enhanced_recommendation.html  # Enhanced AI recommendation
│   ├── workout_detail.html   # Individual workout details
│   ├── profile.html     # User profile management
│   ├── history.html     # Workout history
│   └── analytics.html   # Analytics and insights
└── static/              # Static assets (CSS, JS, images)
```

## 🧠 AI Algorithm Details

### Enhanced Reinforcement Learning Approach
The system uses an **Enhanced Q-Learning** algorithm that models the recommendation problem as a proper RL environment:

1. **State Space**: (fitness_level, fatigue_level, days_since_last, age_group, injury_flag)
2. **Action Space**: Discrete workout intensity levels (low, medium, high) mapped to specific exercises
3. **Reward Function**: Positive for fitness improvement and user comfort, negative for overexertion or injury risk
4. **Q-Learning**: Updates Q-values based on user feedback using ε-greedy policy
5. **Exploration Bonus**: Encourages trying new workouts while learning preferences
6. **Diversity Scoring**: Ensures varied workout recommendations
7. **Persistence**: Q-tables and user profiles saved to disk for continuous learning

### Feature Weights
- **Enjoyment Rating**: 40% (most important)
- **Completion Rate**: 30%
- **Difficulty Rating**: 20%
- **Intensity Level**: 10%

### Learning Process
1. User completes a workout and provides feedback
2. System calculates reward based on weighted feedback
3. Q-values are updated using Q-learning update rule
4. Future recommendations are adjusted accordingly

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
FLASK_SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///workout_recommendations.db
FLASK_ENV=development
```

### Database Configuration
The system uses SQLite by default. To use a different database:

1. Update `app.py` with your database URL
2. Run database migrations if needed
3. Re-seed the database with sample data

## 📈 API Endpoints

### Public Endpoints
- `GET /` - Landing page
- `GET /register` - User registration
- `GET /login` - User login
- `GET /api/workouts` - Get all available workouts

### Protected Endpoints
- `GET /dashboard` - User dashboard
- `GET /recommendations` - Get personalized recommendations
- `GET /health-input` - Health input form for enhanced recommendations
- `POST /health-input` - Submit health inputs and get enhanced recommendation
- `POST /complete-enhanced-workout` - Complete enhanced workout with feedback
- `GET /workout/<id>` - Get workout details
- `POST /complete_workout/<id>` - Complete a workout
- `GET /api/health-progression` - Get health progression data
- `GET /profile` - User profile management
- `GET /history` - Workout history
- `GET /analytics` - Analytics and insights
- `GET /api/recommendations` - API for recommendations

## 🧪 Testing

### Manual Testing
1. Register a new user account
2. Complete several workouts with different feedback
3. Check that recommendations change based on feedback
4. Verify analytics and insights are accurate

### Sample Test Data
The system comes with pre-seeded data including:
- 15+ workout types
- 4 sample users with different fitness levels
- Sample workout history for testing

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production web server (e.g., Gunicorn)
2. Configure environment variables
3. Set up a production database
4. Configure reverse proxy (e.g., Nginx)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Bootstrap for the UI framework
- Chart.js for data visualization
- Font Awesome for icons
- Flask community for the web framework

## 📞 Support

For questions or support, please open an issue on the GitHub repository.

---

**Built with ❤️ using AI and modern web technologies**
