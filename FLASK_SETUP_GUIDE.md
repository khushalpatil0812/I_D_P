# 🌐 Flask Application Setup & Architecture Guide

## 📋 Table of Contents
1. [Flask Framework Overview](#flask-framework-overview)
2. [Project Structure](#project-structure)
3. [Flask Application Setup](#flask-application-setup)
4. [Routing & Blueprints](#routing--blueprints)
5. [Database Integration](#database-integration)
6. [Authentication System](#authentication-system)
7. [Template Engine](#template-engine)
8. [Static Files Management](#static-files-management)
9. [Configuration Management](#configuration-management)
10. [Extensions Used](#extensions-used)

---

## 🎯 Flask Framework Overview

### What is Flask?

**Flask** is a lightweight Python web framework that provides:
- Web server functionality
- URL routing
- Template rendering
- Session management
- Database integration
- Request/response handling

### Why Flask?

✅ **Lightweight**: Minimal setup, quick to start
✅ **Flexible**: Choose your own tools and libraries
✅ **Pythonic**: Clean, readable code
✅ **Well-documented**: Extensive community support
✅ **Scalable**: From simple apps to complex systems

---

## 📁 Project Structure

```
flask-hr-app/
│
├── app.py                          # Main Flask application entry point
├── config.py                       # Configuration settings
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (API keys, secrets)
│
├── models/                         # Database models (ORM)
│   ├── models.py                   # User, Role, IDP, Progress classes
│   └── __pycache__/
│
├── routes/                         # Route handlers (Controllers)
│   ├── auth.py                     # Authentication routes (login, register, logout)
│   ├── hr.py                       # HR management routes
│   ├── employee.py                 # Employee routes
│   └── __pycache__/
│
├── templates/                      # HTML templates (Jinja2)
│   ├── base.html                   # Base template (inherited by all)
│   ├── login.html                  # Login page
│   ├── register.html               # Registration page
│   ├── hr_dashboard.html           # HR dashboard
│   ├── employee_dashboard.html     # Employee dashboard
│   └── ... (other templates)
│
├── static/                         # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css               # Application styles
│   ├── js/
│   │   └── script.js               # Client-side JavaScript
│   └── images/
│
├── ai_engine/                      # AI integration modules
│   ├── gemini_client.py            # Google Gemini API client
│   ├── gap_analysis.py             # Skill gap analysis
│   ├── recommender.py              # IDP recommendations
│   └── __pycache__/
│
├── scripts/                        # Utility scripts
│   ├── init_db.py                  # Database initialization
│   └── check_db.py                 # Database verification
│
├── instance/                       # Instance-specific files
│   └── database.db                 # SQLite database (auto-generated)
│
└── .venv/                          # Virtual environment
    └── ... (Python packages)
```

---

## 🔧 Flask Application Setup

### Step 1: Understanding `app.py` (Main Entry Point)

**File: `app.py`**

```python
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from models.models import db, User
from routes.auth import auth_bp
from routes.hr import hr_bp
from routes.employee import employee_bp
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables FIRST (before anything else)
load_dotenv()

# Initialize Flask application
app = Flask(__name__)

# Load configuration from Config class
app.config.from_object(Config)

# Initialize SQLAlchemy database
db.init_app(app)

# Initialize Flask-Login for authentication
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Redirect to login if not authenticated

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints (route modules)
app.register_blueprint(auth_bp)      # Authentication routes (/login, /register, /logout)
app.register_blueprint(hr_bp)        # HR routes (/hr/*)
app.register_blueprint(employee_bp)  # Employee routes (/employee/*)

# Root route - redirect based on role
@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'hr':
            return redirect(url_for('hr.dashboard'))
        else:
            return redirect(url_for('employee.dashboard'))
    return redirect(url_for('auth.login'))

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Step 2: Configuration (`config.py`)

**File: `config.py`**

```python
import os

class Config:
    # Secret key for session encryption
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    USE_MYSQL = os.environ.get('USE_MYSQL', 'False') == 'True'
    
    if USE_MYSQL:
        # MySQL configuration (if enabled)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.environ.get('DB_USER')}:"
            f"{os.environ.get('DB_PASSWORD')}@"
            f"{os.environ.get('DB_HOST')}/"
            f"{os.environ.get('DB_NAME')}"
        )
    else:
        # SQLite configuration (default)
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance', 'database.db')
    
    # Disable SQLAlchemy modification tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session configuration
    SESSION_COOKIE_HTTPONLY = True    # Prevent JavaScript access to cookies
    SESSION_COOKIE_SAMESITE = 'Lax'   # CSRF protection
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds
```

### Step 3: Environment Variables (`.env`)

**File: `.env`**

```env
# Google Gemini AI API Key
GEMINI_API_KEY=AIzaSyAQ9ydTgkgKs09iOU4_oQgK8AzZQGF60Rw

# Database Configuration
USE_MYSQL=False

# Security
SECRET_KEY=dev-secret-key-change-in-production-ab123cd456ef789

# Session Settings
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=Lax
PERMANENT_SESSION_LIFETIME=86400
```

---

## 🛣️ Routing & Blueprints

### What are Blueprints?

**Blueprints** organize your Flask application into modular components. Instead of one large `app.py`, routes are split into logical modules.

### Blueprint Structure:

```
routes/
├── auth.py       → Authentication (/login, /register, /logout)
├── hr.py         → HR operations (/hr/dashboard, /hr/employees, etc.)
└── employee.py   → Employee operations (/employee/dashboard, /employee/idp/*)
```

### Example: Authentication Blueprint

**File: `routes/auth.py`**

```python
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from models.models import db, User
from werkzeug.security import check_password_hash

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            
            if user.role == 'hr':
                return redirect(url_for('hr.dashboard'))
            else:
                return redirect(url_for('employee.dashboard'))
        else:
            flash('Invalid email or password', 'error')
    
    return render_template('login.html')

# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.register'))
        
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
```

### Example: HR Blueprint

**File: `routes/hr.py`**

```python
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from models.models import db, User, Role, IDP

# Create Blueprint with URL prefix
hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

# Custom decorator to require HR role
def hr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'hr':
            flash('Access denied. HR privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

# HR Dashboard
@hr_bp.route('/dashboard')
@login_required
@hr_required
def dashboard():
    # Get statistics
    total_employees = User.query.filter_by(role='employee').count()
    total_idps = IDP.query.count()
    pending_idps = IDP.query.filter_by(status='pending').count()
    completed_idps = IDP.query.filter_by(status='completed').count()
    
    recent_employees = User.query.filter_by(role='employee')\
                           .order_by(User.created_at.desc())\
                           .limit(5).all()
    
    stats = {
        'total_employees': total_employees,
        'total_idps': total_idps,
        'pending_idps': pending_idps,
        'completed_idps': completed_idps
    }
    
    return render_template('hr_dashboard.html', stats=stats, recent_employees=recent_employees)

# View All Employees
@hr_bp.route('/employees')
@login_required
@hr_required
def employees():
    all_employees = User.query.filter_by(role='employee').all()
    return render_template('hr_employees.html', employees=all_employees)

# Add Employee
@hr_bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
@hr_required
def add_employee():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password', 'password123')
        
        # Create new user
        employee = User(
            name=name,
            email=email,
            role='employee',
            current_role=request.form.get('current_role'),
            target_role=request.form.get('target_role'),
            skills=request.form.get('skills'),
            experience=int(request.form.get('experience', 0)),
            goal=request.form.get('goal')
        )
        employee.set_password(password)
        
        db.session.add(employee)
        db.session.commit()
        
        flash(f'Employee {name} added successfully!', 'success')
        return redirect(url_for('hr.employees'))
    
    roles = Role.query.all()
    return render_template('hr_add_employee.html', roles=roles)
```

### URL Mapping Examples:

```
Route Function                    → URL Path                        → Template
─────────────────────────────────────────────────────────────────────────────────
auth.login()                      → /login                          → login.html
auth.register()                   → /register                       → register.html
auth.logout()                     → /logout                         → (redirect)

hr.dashboard()                    → /hr/dashboard                   → hr_dashboard.html
hr.employees()                    → /hr/employees                   → hr_employees.html
hr.add_employee()                 → /hr/employee/add                → hr_add_employee.html
hr.employee_detail(user_id=2)     → /hr/employee/2                  → hr_employee_detail.html
hr.generate_idp(user_id=2)        → /hr/generate-idp/2              → hr_generate_idp.html
hr.create_manual_idp(user_id=2)   → /hr/create-manual-idp/2         → hr_create_manual_idp.html

employee.dashboard()              → /employee/dashboard             → employee_dashboard.html
employee.profile()                → /employee/profile               → employee_profile.html
employee.idp_detail(idp_id=1)     → /employee/idp/1                 → employee_idp_detail.html
```

---

## 🗄️ Database Integration

### SQLAlchemy ORM Setup

**File: `models/models.py`**

```python
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy instance
db = SQLAlchemy()

# User Model (represents users table)
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    # Columns
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    skills = db.Column(db.Text)
    experience = db.Column(db.Integer, default=0)
    goal = db.Column(db.Text)
    current_role = db.Column(db.String(100))
    target_role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    idps = db.relationship('IDP', backref='user', lazy=True, cascade='all, delete-orphan')
    
    # Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

# IDP Model (represents idps table)
class IDP(db.Model):
    __tablename__ = 'idps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_gap = db.Column(db.Text)
    action = db.Column(db.Text, nullable=False)
    timeline = db.Column(db.String(100))
    metric = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    progress_entries = db.relationship('Progress', backref='idp', lazy=True, cascade='all, delete-orphan')
```

### Database Operations:

```python
# CREATE - Add new record
user = User(name='John', email='john@example.com', role='employee')
user.set_password('password123')
db.session.add(user)
db.session.commit()

# READ - Query records
all_users = User.query.all()                              # Get all users
hr_users = User.query.filter_by(role='hr').all()          # Filter by role
user = User.query.filter_by(email='john@example.com').first()  # Get one user
user = User.query.get(1)                                  # Get by ID

# UPDATE - Modify record
user = User.query.get(1)
user.skills = 'Python, Flask, SQL'
db.session.commit()

# DELETE - Remove record
user = User.query.get(1)
db.session.delete(user)
db.session.commit()

# COMPLEX QUERIES
# Join and filter
idps = IDP.query.join(User).filter(User.role == 'employee').all()

# Count
total_employees = User.query.filter_by(role='employee').count()

# Order by
recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
```

---

## 🔐 Authentication System

### Flask-Login Setup

**Components:**

1. **LoginManager**: Manages user sessions
2. **UserMixin**: Provides default implementations for Flask-Login
3. **@login_required**: Decorator to protect routes
4. **current_user**: Access logged-in user info

### Flow:

```
User Login Attempt
    ↓
User.query.filter_by(email=email).first()  # Find user
    ↓
user.check_password(password)              # Verify password
    ↓
login_user(user, remember=True)            # Create session
    ↓
Redirect to appropriate dashboard
```

### Session Management:

```python
# In config.py
SESSION_COOKIE_HTTPONLY = True    # Prevents JavaScript from accessing cookie
SESSION_COOKIE_SAMESITE = 'Lax'   # Protects against CSRF attacks
PERMANENT_SESSION_LIFETIME = 86400 # Session expires after 24 hours

# In routes/auth.py
login_user(user, remember=True)   # Creates persistent session
logout_user()                     # Destroys session
```

### Protected Routes:

```python
from flask_login import login_required, current_user

@app.route('/protected')
@login_required  # Must be logged in to access
def protected_route():
    return f'Hello {current_user.name}!'

# Role-based protection
def hr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'hr':
            flash('Access denied', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
```

---

## 🎨 Template Engine (Jinja2)

### Template Inheritance

**Base Template: `templates/base.html`**

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}IDP System{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <nav>
        {% if current_user.is_authenticated %}
            {% if current_user.role == 'hr' %}
                <a href="{{ url_for('hr.dashboard') }}">Dashboard</a>
                <a href="{{ url_for('hr.employees') }}">Employees</a>
            {% else %}
                <a href="{{ url_for('employee.dashboard') }}">Dashboard</a>
                <a href="{{ url_for('employee.profile') }}">Profile</a>
            {% endif %}
            <a href="{{ url_for('auth.logout') }}">Logout</a>
        {% endif %}
    </nav>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

**Child Template: `templates/hr_dashboard.html`**

```html
{% extends "base.html" %}

{% block title %}HR Dashboard{% endblock %}

{% block content %}
<h1>HR Dashboard</h1>
<p>Total Employees: {{ stats.total_employees }}</p>
<p>Total IDPs: {{ stats.total_idps }}</p>

{% for employee in recent_employees %}
    <div>{{ employee.name }} - {{ employee.email }}</div>
{% endfor %}
{% endblock %}
```

### Jinja2 Features Used:

```html
<!-- Variables -->
{{ current_user.name }}
{{ stats.total_employees }}

<!-- Conditionals -->
{% if current_user.is_authenticated %}
    Welcome back!
{% else %}
    Please login
{% endif %}

<!-- Loops -->
{% for employee in employees %}
    <div>{{ employee.name }}</div>
{% endfor %}

<!-- URL Generation -->
<a href="{{ url_for('hr.dashboard') }}">Dashboard</a>
<a href="{{ url_for('hr.employee_detail', user_id=employee.id) }}">View</a>

<!-- Static Files -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>

<!-- Filters -->
{{ employee.skills[:30] }}  <!-- Slice -->
{{ idp.created_at.strftime('%Y-%m-%d') }}  <!-- Date format -->
```

---

## 📦 Static Files Management

### Directory Structure:

```
static/
├── css/
│   └── style.css       # All application styles
├── js/
│   └── script.js       # Client-side JavaScript
└── images/
    └── logo.png        # Images and assets
```

### Accessing Static Files:

```html
<!-- In templates -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
<script src="{{ url_for('static', filename='js/script.js') }}"></script>
<img src="{{ url_for('static', filename='images/logo.png') }}">
```

### Flask automatically serves files from `static/` folder:
- `http://127.0.0.1:5000/static/css/style.css`
- `http://127.0.0.1:5000/static/js/script.js`

---

## ⚙️ Configuration Management

### Environment-Based Configuration:

```python
# Development
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Production
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:pass@server/db'
```

### Loading from Environment Variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

SECRET_KEY = os.environ.get('SECRET_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
```

---

## 🧩 Flask Extensions Used

### 1. Flask-SQLAlchemy
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
```
**Purpose**: Database ORM (Object-Relational Mapping)

### 2. Flask-Login
```python
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
```
**Purpose**: User session management and authentication

### 3. Werkzeug
```python
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
```
**Purpose**: Security utilities (password hashing, file uploads)

### 4. python-dotenv
```python
from dotenv import load_dotenv
load_dotenv()
```
**Purpose**: Load environment variables from `.env` file

---

## 🚀 Running the Flask Application

### Development Mode:

```bash
# Activate virtual environment
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Mac/Linux

# Run Flask app
python app.py

# Flask runs on:
# http://127.0.0.1:5000 (localhost)
# http://0.0.0.0:5000 (all network interfaces)
```

### Debug Mode Features:

When `debug=True`:
- ✅ Auto-reload on code changes
- ✅ Detailed error pages
- ✅ Interactive debugger
- ⚠️ **Never use in production!**

### Production Mode:

```python
# In app.py, change:
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

Use production WSGI server:
```bash
# Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Waitress (Windows)
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

---

## 📊 Request-Response Cycle

```
1. Client Request
   └─→ Browser: GET http://127.0.0.1:5000/hr/dashboard

2. Flask Routing
   └─→ Matches route: @hr_bp.route('/dashboard')
   └─→ Calls function: hr.dashboard()

3. Authentication Check
   └─→ @login_required decorator checks session
   └─→ @hr_required decorator checks user role

4. Business Logic
   └─→ Query database: User.query.filter_by(role='employee').count()
   └─→ Process data: Calculate statistics

5. Template Rendering
   └─→ render_template('hr_dashboard.html', stats=stats)
   └─→ Jinja2 processes template with data

6. HTTP Response
   └─→ HTML sent to browser
   └─→ Status: 200 OK

7. Browser Renders
   └─→ Displays dashboard with data
```

---

## 🛠️ Common Flask Patterns

### Flash Messages:
```python
from flask import flash

flash('Employee added successfully!', 'success')
flash('Error occurred', 'error')
flash('Warning message', 'warning')
```

### Redirects:
```python
from flask import redirect, url_for

return redirect(url_for('hr.dashboard'))
return redirect(url_for('hr.employee_detail', user_id=2))
```

### Request Data:
```python
from flask import request

# GET parameters
search = request.args.get('search')

# POST form data
email = request.form.get('email')

# Files
file = request.files['file']

# JSON data
data = request.get_json()
```

### Session Data:
```python
from flask import session

# Store in session
session['user_id'] = 123

# Retrieve from session
user_id = session.get('user_id')

# Remove from session
session.pop('user_id', None)
```

---

## 📚 Summary

### Flask Setup Checklist:

- [x] Install Flask and extensions
- [x] Create `app.py` (main application)
- [x] Set up `config.py` (configuration)
- [x] Create `.env` (environment variables)
- [x] Define models in `models/models.py`
- [x] Create blueprints in `routes/`
- [x] Design templates in `templates/`
- [x] Add static files in `static/`
- [x] Initialize database
- [x] Run application

### Key Flask Concepts:

1. **Application Factory**: Initialize Flask app with extensions
2. **Blueprints**: Modular route organization
3. **ORM**: Database operations with SQLAlchemy
4. **Authentication**: User management with Flask-Login
5. **Templates**: HTML rendering with Jinja2
6. **Static Files**: CSS, JS, images serving
7. **Configuration**: Environment-based settings

---

**Your Flask application is fully configured and ready to run!** 🎉
