from flask import Blueprint

tasks = Blueprint('tasks', __name__)

from . import routes

task_bp = Blueprint(
    'task_bp',
    __name__,
    url_prefix='/tasks',
    template_folder='../templates/tasks'  # example path
)
