from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
from ..models import User
from .forms import LoginForm, RegisterForm, ForgotPasswordForm

# Define the Blueprint
auth_bp = Blueprint('auth', __name__, template_folder='templates')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data.strip()
        email = form.email.data.strip().lower()
        password = form.password.data
        confirm_password = form.confirm_password.data
        role = form.role.data

        errors = []

        if password != confirm_password:
            errors.append("Passwords do not match.")

        if User.query.filter_by(email=email).first():
            errors.append("Email is already registered.")

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html', form=form)

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('user_management.dashboard'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')

            # Redirect based on user role
            if user.role == 'admin':
                return redirect(url_for('user_management.dashboard'))  # Admin dashboard
            else:
                return redirect(url_for('tasks.dashboard'))
  # Employee dashboard

        elif user:
            flash('Incorrect password.', 'danger')
        else:
            flash('Email not found.', 'danger')
    elif request.method == 'POST':
        flash('Please correct the errors and try again.', 'danger')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        user = User.query.filter_by(email=email).first()
        if user:
            flash('A password reset link has been sent to your email.', 'info')
            # Placeholder for email logic
        else:
            flash('Email not found.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    return render_template('auth/forgot_password.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
