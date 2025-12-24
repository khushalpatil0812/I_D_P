"""
Simple database checker and user creator
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from models.models import db, User, Role

def check_and_create_users():
    app = create_app()
    
    with app.app_context():
        # Check existing users
        users = User.query.all()
        print(f"\n=== Current Users in Database ===")
        print(f"Total users: {len(users)}")
        
        for user in users:
            print(f"\nUser ID: {user.id}")
            print(f"  Name: {user.name}")
            print(f"  Email: {user.email}")
            print(f"  Role: {user.role}")
            print(f"  Has Password Hash: {bool(user.password_hash)}")
        
        # Test passwords
        if users:
            print(f"\n=== Testing Password Authentication ===")
            hr_user = User.query.filter_by(email='hr@company.com').first()
            if hr_user:
                print(f"HR User found: {hr_user.email}")
                print(f"  Password 'hr123' check: {hr_user.check_password('hr123')}")
            
            emp_user = User.query.filter_by(email='john@company.com').first()
            if emp_user:
                print(f"Employee User found: {emp_user.email}")
                print(f"  Password 'emp123' check: {emp_user.check_password('emp123')}")
        
        # Create users if they don't exist
        if len(users) == 0:
            print(f"\n=== Creating Default Users ===")
            
            hr_user = User(
                name='HR Admin',
                email='hr@company.com',
                role='hr'
            )
            hr_user.set_password('hr123')
            db.session.add(hr_user)
            
            employee = User(
                name='John Doe',
                email='john@company.com',
                role='employee',
                skills='Python, HTML, CSS',
                experience=2,
                goal='Become a Full Stack Developer',
                current_role='Junior Developer',
                target_role='Full Stack Developer'
            )
            employee.set_password('emp123')
            db.session.add(employee)
            
            db.session.commit()
            print("✅ Users created successfully!")
        
        print(f"\n=== Database Check Complete ===\n")

if __name__ == '__main__':
    check_and_create_users()
