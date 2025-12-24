import sys
sys.path.insert(0, 'D:/downloads/flask-hr-app')

from dotenv import load_dotenv
load_dotenv()

from app import create_app
from models.models import db, User

app = create_app()

with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
    
    for user in users:
        print(f"\nEmail: {user.email}")
        print(f"Role: {user.role}")
        print(f"Password check 'hr123': {user.check_password('hr123')}")
        print(f"Password check 'emp123': {user.check_password('emp123')}")
