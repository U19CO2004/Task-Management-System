# from flask import render_template, redirect, url_for, request, flash
# from flask_login import login_user, logout_user, login_required, current_user

# from app.user_management import user_management_bp
# from app.models import User
# from app import db
# from datetime import datetime

# from app.auth.forms import LoginForm  # import it properly

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db
from datetime import datetime
from app.auth.forms import LoginForm
from werkzeug.security import generate_password_hash

user_management_bp = Blueprint('user_management', __name__, url_prefix='/admin')

# --------------------------
# Auth Routes
# --------------------------

@user_management_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('user_management.dashboard'))
        flash('Invalid credentials', 'danger')

    return render_template('auth/login.html', form=form)

@user_management_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_management.login'))

# --------------------------
# Dashboard Route
# --------------------------

@user_management_bp.route('/dashboard')
@login_required
def dashboard():
    from app.models import Task

    if current_user.role == 'admin':
        users = User.query.all()
        tasks_query = Task.query.all()
    else:
        users = None
        tasks_query = Task.query.filter_by(assigned_to=current_user.id).all()

    task_stats = {
        'employee_count': User.query.filter_by(role='employee').count() if current_user.role == 'admin' else None,
        'total': len(tasks_query),
        'overdue': len([
            t for t in tasks_query
            if t.deadline and t.deadline < datetime.utcnow() and t.status != 'Completed'
        ]),
        'no_deadline': len([t for t in tasks_query if not t.deadline]),
        'due_today': len([t for t in tasks_query if t.deadline and t.deadline.date() == datetime.utcnow().date()]),
        'pending': len([t for t in tasks_query if t.status == 'Pending']),
        'in_progress': len([t for t in tasks_query if t.status == 'In progress']),
        'completed': len([t for t in tasks_query if t.status == 'Completed']),
        'notifications': 5  # Static placeholder
    }

    return render_template('user_management/dashboard.html', task_stats=task_stats, users=users)

# --------------------------
# Manage Users Routes (Admin Only)
# --------------------------

def admin_required():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash("Access denied. Admins only.", "danger")
        return False
    return True

@user_management_bp.route('/manage-users')
@login_required
def manage_users():
    if not admin_required():
        return redirect(url_for('user_management.dashboard'))

    users = User.query.all()
    return render_template('user_management/manage_users.html', users=users)


from werkzeug.security import generate_password_hash

@user_management_bp.route('/add-user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully.', 'success')
        return redirect(url_for('user_management.manage_users'))

    return render_template('user_management/add_user.html')

@user_management_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not admin_required():
        return redirect(url_for('user_management.dashboard'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')

        if not user.username or not user.email or not user.role:
            flash("All fields are required.", "warning")
            return render_template('user_management/edit_user.html', user=user)

        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for('user_management.manage_users'))

    return render_template('user_management/edit_user.html', user=user)

@user_management_bp.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully.', 'success')
    return redirect(url_for('user_management.manage_users'))


@user_management_bp.route('/profile')
@login_required
def profile():
    return render_template('user_management/profile.html', user=current_user)


# from flask import Blueprint, render_template, request, redirect, url_for, flash
# from flask_login import login_required
# from app import db
# from app.models import Task, User  # Adjust according to your structure

# # Blueprint definition
# tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='../templates/tasks')

# # Route for creating a task
# @tasks_bp.route('/add-task', methods=['GET', 'POST'])
# @login_required
# def create_task():
#     users = User.query.all()

#     if request.method == 'POST':
#         title = request.form.get('title')
#         description = request.form.get('description')
#         assigned_to = request.form.get('assigned_to')
#         deadline = request.form.get('deadline')

#         if not title or not assigned_to:
#             flash("Title and Assigned User are required!", "danger")
#             return redirect(url_for('tasks.create_task'))

#         try:
#             new_task = Task(
#                 title=title,
#                 description=description,
#                 assigned_to=int(assigned_to),
#                 deadline=deadline
#             )
#             db.session.add(new_task)
#             db.session.commit()
#             flash("Task created successfully!", "success")
#             return redirect(url_for('tasks.create_task'))
#         except Exception as e:
#             db.session.rollback()
#             flash(f"Error creating task: {str(e)}", "danger")
#             return redirect(url_for('tasks.create_task'))

#     return render_template('tasks/add_task.html', users=users)
