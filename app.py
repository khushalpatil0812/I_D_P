from dotenv import load_dotenv

# Load environment variables BEFORE importing Config
load_dotenv()

from flask import Flask
from flask_login import LoginManager
from config import Config
from models.models import db, User
from routes.auth import auth_bp
from routes.hr import hr_bp
from routes.employee import employee_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Session configuration for proper login
    app.config['SESSION_COOKIE_SECURE'] = False
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['REMEMBER_COOKIE_DURATION'] = 3600 * 24  # 24 hours
    
    # Initialize database
    db.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(hr_bp)
    app.register_blueprint(employee_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default users if none exist
        if User.query.count() == 0:
            # Create HR user
            hr_user = User(
                name='HR Admin',
                email='hr@company.com',
                role='hr'
            )
            hr_user.set_password('hr123')
            
            # Create sample employee
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
            
            db.session.add(hr_user)
            db.session.add(employee)
            db.session.commit()
            
            print("Default users created:")
            print("HR: hr@company.com / hr123")
            print("Employee: john@company.com / emp123")
        
        # Create sample roles if none exist
        from models.models import Role
        if Role.query.count() == 0:
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
            
            db.session.commit()
            print("Sample roles created")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
