from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from functools import wraps
from models.models import db, IDP, Progress

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

def employee_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please login to continue', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@employee_bp.route('/dashboard')
@login_required
@employee_required
def dashboard():
    user_idps = IDP.query.filter_by(user_id=current_user.id).all()
    
    stats = {
        'total': len(user_idps),
        'pending': len([idp for idp in user_idps if idp.status == 'pending']),
        'in_progress': len([idp for idp in user_idps if idp.status == 'in_progress']),
        'completed': len([idp for idp in user_idps if idp.status == 'completed'])
    }
    
    return render_template('employee_dashboard.html', idps=user_idps, stats=stats)

@employee_bp.route('/idp/<int:idp_id>')
@login_required
@employee_required
def idp_detail(idp_id):
    idp = IDP.query.get_or_404(idp_id)
    
    if idp.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('employee.dashboard'))
    
    progress = Progress.query.filter_by(idp_id=idp.id).order_by(Progress.updated_at.desc()).first()
    
    return render_template('employee_idp_detail.html', idp=idp, progress=progress)

@employee_bp.route('/idp/<int:idp_id>/progress', methods=['GET'])
@login_required
@employee_required
def progress_page(idp_id):
    idp = IDP.query.get_or_404(idp_id)
    
    if idp.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('employee.dashboard'))
    
    progress = Progress.query.filter_by(idp_id=idp.id).order_by(Progress.updated_at.desc()).first()
    
    return render_template('employee_progress_update.html', idp=idp, progress=progress)

@employee_bp.route('/idp/<int:idp_id>/update', methods=['POST'])
@login_required
@employee_required
def update_progress(idp_id):
    idp = IDP.query.get_or_404(idp_id)
    
    if idp.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('employee.dashboard'))
    
    completion = request.form.get('completion', 0, type=int)
    feedback = request.form.get('feedback', '')
    status = request.form.get('status', idp.status)
    
    # Update IDP status
    idp.status = status
    
    # Create or update progress entry
    progress = Progress.query.filter_by(idp_id=idp.id).first()
    if progress:
        progress.completion = completion
        progress.feedback = feedback
    else:
        progress = Progress(
            idp_id=idp.id,
            completion=completion,
            feedback=feedback
        )
        db.session.add(progress)
    
    db.session.commit()
    
    flash('Progress updated successfully!', 'success')
    return redirect(url_for('employee.idp_detail', idp_id=idp_id))

@employee_bp.route('/profile')
@login_required
@employee_required
def profile():
    return render_template('employee_profile.html', user=current_user)

@employee_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@employee_required
def edit_profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name', current_user.name)
        current_user.skills = request.form.get('skills', current_user.skills)
        current_user.experience = request.form.get('experience', current_user.experience, type=int)
        current_user.goal = request.form.get('goal', current_user.goal)
        current_user.current_role = request.form.get('current_role', current_user.current_role)
        current_user.target_role = request.form.get('target_role', current_user.target_role)
        
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('employee.profile'))
    
    return render_template('employee_edit_profile.html', user=current_user)
