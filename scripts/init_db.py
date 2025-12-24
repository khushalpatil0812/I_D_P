"""
Database initialization script
Run this to create tables and seed initial data
"""
import sys
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models.models import db, User, Role
import pandas as pd

def init_database():
    app = create_app()
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Check if users already exist
        if User.query.count() > 0:
            print("Database already initialized!")
            return
        
        print("Seeding default data...")
        
        # Create HR user
        hr_user = User(
            name='HR Admin',
            email='hr@company.com',
            role='hr'
        )
        hr_user.set_password('hr123')
        db.session.add(hr_user)
        
        # Create sample roles
        roles_data = [
            {
                'role_name': 'Full Stack Developer',
                'required_skills': 'Python, JavaScript, React, Node.js, SQL, Git, REST APIs, Docker',
                'description': 'Develops both frontend and backend applications'
            },
            {
                'role_name': 'Data Scientist',
                'required_skills': 'Python, Machine Learning, Statistics, SQL, Data Visualization, Pandas, NumPy',
                'description': 'Analyzes data and builds ML models'
            },
            {
                'role_name': 'DevOps Engineer',
                'required_skills': 'Linux, Docker, Kubernetes, CI/CD, AWS, Terraform, Monitoring',
                'description': 'Manages infrastructure and deployment pipelines'
            }
        ]
        
        for role_data in roles_data:
            role = Role(**role_data)
            db.session.add(role)
        
        # Load employees from CSV if exists
        csv_path = os.path.join('data', 'sample_employees.csv')
        if os.path.exists(csv_path):
            print(f"Loading employees from {csv_path}...")
            df = pd.read_csv(csv_path)
            
            for _, row in df.iterrows():
                user = User(
                    name=row['name'],
                    email=row['email'],
                    role='employee',
                    skills=row['skills'],
                    experience=int(row['experience']),
                    goal=row['goal'],
                    current_role=row['current_role'],
                    target_role=row['target_role']
                )
                user.set_password(row['password'])
                db.session.add(user)
        
        db.session.commit()
        print("✅ Database initialized successfully!")
        print("\nDefault users:")
        print("HR: hr@company.com / hr123")
        print("Employees loaded from CSV")

if __name__ == '__main__':
    init_database()
