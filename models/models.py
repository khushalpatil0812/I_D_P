from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')  # 'hr' or 'employee'
    skills = db.Column(db.Text)  # Comma-separated skills
    experience = db.Column(db.Integer, default=0)  # Years of experience
    goal = db.Column(db.Text)  # Career goal
    current_role = db.Column(db.String(100))
    target_role = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    idps = db.relationship('IDP', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_skills_list(self):
        return [s.strip() for s in self.skills.split(',') if s.strip()] if self.skills else []
    
    def __repr__(self):
        return f'<User {self.email}>'


class Role(db.Model):
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(100), unique=True, nullable=False)
    required_skills = db.Column(db.Text)  # Comma-separated required skills
    description = db.Column(db.Text)
    
    def get_required_skills_list(self):
        return [s.strip() for s in self.required_skills.split(',') if s.strip()] if self.required_skills else []
    
    def __repr__(self):
        return f'<Role {self.role_name}>'


class IDP(db.Model):
    __tablename__ = 'idps'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_gap = db.Column(db.Text)  # JSON or comma-separated missing skills
    action = db.Column(db.Text, nullable=False)  # SMART action
    timeline = db.Column(db.String(100))  # Time-bound goal
    metric = db.Column(db.String(255))  # Measurable metric
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    progress_entries = db.relationship('Progress', backref='idp', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<IDP {self.id} for User {self.user_id}>'


class Progress(db.Model):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    idp_id = db.Column(db.Integer, db.ForeignKey('idps.id'), nullable=False)
    completion = db.Column(db.Integer, default=0)  # Percentage 0-100
    feedback = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Progress {self.id} for IDP {self.idp_id}>'
