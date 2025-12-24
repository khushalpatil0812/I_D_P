from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from models.models import db, User, Role, IDP
from ai_engine.recommender import generate_smart_recommendations
import pandas as pd
import os
from werkzeug.utils import secure_filename

hr_bp = Blueprint('hr', __name__, url_prefix='/hr')

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def hr_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'hr':
            flash('Access denied. HR privileges required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@hr_bp.route('/dashboard')
@login_required
@hr_required
def dashboard():
    total_employees = User.query.filter_by(role='employee').count()
    total_idps = IDP.query.count()
    pending_idps = IDP.query.filter_by(status='pending').count()
    completed_idps = IDP.query.filter_by(status='completed').count()
    
    recent_employees = User.query.filter_by(role='employee').order_by(User.created_at.desc()).limit(5).all()
    
    stats = {
        'total_employees': total_employees,
        'total_idps': total_idps,
        'pending_idps': pending_idps,
        'completed_idps': completed_idps
    }
    
    return render_template('hr_dashboard.html', stats=stats, recent_employees=recent_employees)

@hr_bp.route('/employees')
@login_required
@hr_required
def employees():
    all_employees = User.query.filter_by(role='employee').all()
    return render_template('hr_employees.html', employees=all_employees)

@hr_bp.route('/employee/<int:user_id>')
@login_required
@hr_required
def employee_detail(user_id):
    employee = User.query.get_or_404(user_id)
    if employee.role != 'employee':
        flash('Invalid employee', 'error')
        return redirect(url_for('hr.employees'))
    
    idps = IDP.query.filter_by(user_id=user_id).all()
    return render_template('hr_employee_detail.html', employee=employee, idps=idps)

@hr_bp.route('/employee/add', methods=['GET', 'POST'])
@login_required
@hr_required
def add_employee():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password', 'password123')
        skills = request.form.get('skills', '')
        experience = request.form.get('experience', 0, type=int)
        goal = request.form.get('goal', '')
        current_role = request.form.get('current_role', '')
        target_role = request.form.get('target_role', '')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('hr.add_employee'))
        
        user = User(
            name=name,
            email=email,
            role='employee',
            skills=skills,
            experience=experience,
            goal=goal,
            current_role=current_role,
            target_role=target_role
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'Employee {name} added successfully!', 'success')
        return redirect(url_for('hr.employees'))
    
    roles = Role.query.all()
    return render_template('hr_add_employee.html', roles=roles)

@hr_bp.route('/upload-csv', methods=['GET', 'POST'])
@login_required
@hr_required
def upload_csv():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file uploaded', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            try:
                # Read CSV file
                df = pd.read_csv(file)
                
                # Validate required columns
                required_columns = ['name', 'email']
                if not all(col in df.columns for col in required_columns):
                    flash(f'CSV must contain columns: {", ".join(required_columns)}', 'error')
                    return redirect(request.url)
                
                added_count = 0
                skipped_count = 0
                
                # Process each row
                for index, row in df.iterrows():
                    email = str(row['email']).strip()
                    name = str(row['name']).strip()
                    
                    # Check if user already exists
                    if User.query.filter_by(email=email).first():
                        skipped_count += 1
                        continue
                    
                    # Create new employee
                    user = User(
                        name=name,
                        email=email,
                        role='employee',
                        skills=str(row.get('skills', '')).strip(),
                        experience=int(row.get('experience', 0)),
                        goal=str(row.get('goal', '')).strip(),
                        current_role=str(row.get('current_role', '')).strip(),
                        target_role=str(row.get('target_role', '')).strip()
                    )
                    
                    # Set password (default or from CSV)
                    password = str(row.get('password', 'password123')).strip()
                    user.set_password(password)
                    
                    db.session.add(user)
                    added_count += 1
                
                db.session.commit()
                
                flash(f'CSV processed: {added_count} employees added, {skipped_count} skipped (already exist)', 'success')
                return redirect(url_for('hr.employees'))
                
            except Exception as e:
                flash(f'Error processing CSV: {str(e)}', 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload a CSV file.', 'error')
            return redirect(request.url)
    
    return render_template('hr_upload_csv.html')

@hr_bp.route('/generate-idp/<int:user_id>', methods=['GET', 'POST'])
@login_required
@hr_required
def generate_idp(user_id):
    employee = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        target_role_name = request.form.get('target_role')
        
        # Update employee target role
        employee.target_role = target_role_name
        db.session.commit()
        
        # Find the role and its required skills
        target_role = Role.query.filter_by(role_name=target_role_name).first()
        
        if not target_role:
            flash('Target role not found. Using manual skill input.', 'warning')
            required_skills = request.form.get('required_skills', '').split(',')
            required_skills = [s.strip() for s in required_skills if s.strip()]
        else:
            required_skills = target_role.get_required_skills_list()
        
        if not required_skills:
            flash('No required skills defined for this role', 'error')
            return redirect(url_for('hr.employee_detail', user_id=user_id))
        
        # Generate SMART recommendations
        recommendations = generate_smart_recommendations(employee, target_role_name, required_skills)
        
        # Save IDPs to database
        for rec in recommendations:
            idp = IDP(
                user_id=employee.id,
                skill_gap=rec['skill_gap'],
                action=rec['action'],
                timeline=rec['timeline'],
                metric=rec['metric'],
                status=rec['status']
            )
            db.session.add(idp)
        
        db.session.commit()
        
        flash(f'IDP generated successfully for {employee.name}!', 'success')
        return redirect(url_for('hr.employee_detail', user_id=user_id))
    
    roles = Role.query.all()
    return render_template('hr_generate_idp.html', employee=employee, roles=roles)

@hr_bp.route('/create-manual-idp/<int:user_id>', methods=['GET', 'POST'])
@login_required
@hr_required
def create_manual_idp(user_id):
    """Manually create IDP without AI generation"""
    employee = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        skill_gap = request.form.get('skill_gap')
        action = request.form.get('action')
        timeline = request.form.get('timeline')
        metric = request.form.get('metric')
        status = request.form.get('status', 'not_started')
        
        # Validate required fields
        if not all([skill_gap, action, timeline, metric]):
            flash('All fields are required to create an IDP', 'error')
            return redirect(url_for('hr.create_manual_idp', user_id=user_id))
        
        # Create IDP
        idp = IDP(
            user_id=employee.id,
            skill_gap=skill_gap,
            action=action,
            timeline=timeline,
            metric=metric,
            status=status
        )
        db.session.add(idp)
        db.session.commit()
        
        flash(f'Manual IDP created successfully for {employee.name}!', 'success')
        return redirect(url_for('hr.employee_detail', user_id=user_id))
    
    return render_template('hr_create_manual_idp.html', employee=employee)

@hr_bp.route('/roles')
@login_required
@hr_required
def roles():
    all_roles = Role.query.all()
    return render_template('hr_roles.html', roles=all_roles)

@hr_bp.route('/role/add', methods=['GET', 'POST'])
@login_required
@hr_required
def add_role():
    if request.method == 'POST':
        role_name = request.form.get('role_name')
        required_skills = request.form.get('required_skills')
        description = request.form.get('description', '')
        
        if Role.query.filter_by(role_name=role_name).first():
            flash('Role already exists', 'error')
            return redirect(url_for('hr.add_role'))
        
        role = Role(
            role_name=role_name,
            required_skills=required_skills,
            description=description
        )
        
        db.session.add(role)
        db.session.commit()
        
        flash(f'Role "{role_name}" added successfully!', 'success')
        return redirect(url_for('hr.roles'))
    
    return render_template('hr_add_role.html')

@hr_bp.route('/reports')
@login_required
@hr_required
def reports():
    # Aggregate statistics
    all_idps = IDP.query.all()
    all_employees = User.query.filter_by(role='employee').all()
    
    idp_by_status = {
        'pending': IDP.query.filter_by(status='pending').count(),
        'in_progress': IDP.query.filter_by(status='in_progress').count(),
        'completed': IDP.query.filter_by(status='completed').count()
    }
    
    return render_template('hr_reports.html', idp_by_status=idp_by_status, 
                         total_employees=len(all_employees), total_idps=len(all_idps))
