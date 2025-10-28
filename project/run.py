#!/usr/bin/env python3
"""
FitRec AI - Workout Recommendation System
Run script for easy application startup
"""

import os
import sys
from app import create_app

def main():
    """Main function to run the application"""
    print("🏋️  FitRec AI - Workout Recommendation System")
    print("=" * 50)
    
    # Create Flask app
    app = create_app()
    
    # Run the application
    print("🚀 Starting FitRec AI...")
    print("📱 Open your browser and go to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down FitRec AI...")
        sys.exit(0)

if __name__ == '__main__':
    main()
