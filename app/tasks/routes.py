
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime

from .forms import TaskForm
from app.models import Task, User
from app import db

# Blueprint
tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

user_bp = Blueprint('user', __name__)
# -------------------------------
# Add Task Route
# -------------------------------
@tasks_bp.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            assigned_to=form.assigned_to.data,
            deadline=form.deadline.data,
            status=form.status.data,
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully.', 'success')
        return redirect(url_for('tasks.dashboard'))

    elif request.method == 'POST':
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"{getattr(form, field).label.text}: {error}", 'danger')

    return render_template('tasks/add_task.html', form=form)


# -------------------------------
# Dashboard Route
# -------------------------------
@tasks_bp.route('/dashboard')
@login_required
def dashboard():
    today = datetime.utcnow().date()

    if current_user.role == 'admin':
        users = User.query.all()
        tasks_query = Task.query.all() 
        template = 'tasks/dashboard.html'
    else:
        users = None
        tasks_query = Task.query.filter_by(assigned_to=current_user.id).all()
        template = 'tasks/user_dashboard.html'

    task_stats = {
        'employee_count': User.query.filter_by(role='employee').count() if current_user.role == 'admin' else None,
        'total': len(tasks_query),
        'overdue': len([t for t in tasks_query if t.deadline and t.deadline < datetime.utcnow() and t.status != 'Completed']),
        'no_deadline': len([t for t in tasks_query if not t.deadline]),
        'due_today': len([t for t in tasks_query if t.deadline and t.deadline.date() == datetime.utcnow().date()]),
        'pending': len([t for t in tasks_query if t.status == 'Pending']),
        'in_progress': len([t for t in tasks_query if t.status == 'In progress']),
        'completed': len([t for t in tasks_query if t.status == 'Completed']),
        'notifications': 5  # static placeholder
    }
    return render_template(template, task_stats=task_stats, users=users)

# -------------------------------
# My Task Route (Employee Only)
# -------------------------------
@tasks_bp.route('/my-task')
@login_required
def user_tasks():
    tasks = Task.query.filter_by(assigned_to=current_user.id).all()
    return render_template('tasks/my_task.html', tasks=tasks)



# -------------------------------
# Manage Users (Admin Only)
# -------------------------------
@tasks_bp.route('/manage-users')
@login_required
def manage_users():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user_management.dashboard'))

    users = User.query.filter(User.role == 'employee').all()
    return render_template('tasks/manage_users.html', users=users)


# -------------------------------
# Edit User (Admin Only)
# -------------------------------
@tasks_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user_management.dashboard'))

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        new_email = request.form['email']
        new_username = request.form['username']
        new_password = request.form['password']

        user.email = new_email
        user.username = new_username
        if new_password:
            user.password = generate_password_hash(new_password)

        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('user_management.manage_users'))

    return render_template('edit_user.html', user=user)


# -------------------------------
# Delete User (Admin Only)
# -------------------------------
@tasks_bp.route('/delete_user/<int:user_id>')
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('user_management.dashboard'))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('user_management.manage_users'))


# -------------------------------
# Notifications Route (Optional)
# -------------------------------
@tasks_bp.route('/notifications')
@login_required
def notifications():
    notifications = []  # Placeholder - customize later
    return render_template('tasks/notifications.html', notifications=notifications)


# -------------------------------
# All Tasks Route (Admin & Employee)
# -------------------------------
@tasks_bp.route('/all-tasks')
@login_required
def all_tasks():
    if current_user.role == 'admin':
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(assigned_to=current_user.id).all()

    return render_template('tasks/all_tasks.html', tasks=tasks)



@tasks_bp.route('/edit-task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm(obj=task)
    form.assigned_to.choices = [(user.id, user.username) for user in User.query.all()]

    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.assigned_to = form.assigned_to.data
        task.deadline = form.deadline.data
        task.status = form.status.data
        db.session.commit()
        flash('Task updated successfully.', 'success')
        return redirect(url_for('tasks.all_tasks'))

    return render_template('tasks/edit_task.html', form=form, task=task)



@tasks_bp.route('/delete-task/<int:task_id>')
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully.', 'success')
    return redirect(url_for('tasks.all_tasks'))


@tasks_bp.route('/filter/<string:filter_type>')
@login_required
def filter_tasks(filter_type):
    today = datetime.today().date()
    
    if filter_type == 'due_today':
        tasks = Task.query.filter(db.func.date(Task.deadline) == today).all()
    elif filter_type == 'overdue':
        tasks = Task.query.filter(Task.deadline < today).all()
    elif filter_type == 'no_deadline':
        tasks = Task.query.filter(Task.deadline == None).all()
    else:
        tasks = Task.query.all()

    return render_template('tasks/all_tasks.html', tasks=tasks)



@user_bp.route('/user/tasks')
@login_required
def user_tasks():
    tasks = Task.query.filter_by(assigned_to=current_user.username).all()
    return render_template('user/user_tasks.html', tasks=tasks)

# app/tasks/routes.py

# from flask import Blueprint, render_template, request, redirect, url_for

# tasks_bp = Blueprint(
#     'tasks_bp',
#     __name__,
#     url_prefix='/tasks',
#     template_folder='templates/tasks'  # or adjust path as needed
# )

# @tasks_bp.route('/')
# def task_dashboard():
#     return render_template('tasks/dashboard.html')
