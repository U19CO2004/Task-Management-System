from flask import Blueprint

user_management_bp = Blueprint(
    'user_management',
    __name__,
    url_prefix='/user',
    template_folder='../templates/user_management'
)

