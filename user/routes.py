# app/user/routes.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

tasks = Blueprint('tasks', __name__)

@tasks.route('/my-tasks')  # This is the route URL
@login_required
def user_tasks():
    # Your logic here, e.g., fetch user-specific tasks
    return render_template('tasks/my_tasks.html')
