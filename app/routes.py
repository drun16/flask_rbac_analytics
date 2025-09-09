# app/routes.py
from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.urls import url_parse
from urllib.parse import urlparse
from app import db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Role, LoginEvent
from app.decorators import admin_required

# Create a Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'danger')
            return redirect(url_for('main.login'))
        
        login_user(user, remember=form.remember_me.data)
        
        # --- Analytics: Record Login Event ---
        login_event = LoginEvent(user_id=user.id)
        db.session.add(login_event)
        db.session.commit()
        # ------------------------------------

        # Redirect to the page the user was trying to access, or dashboard
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.dashboard')
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user_role = Role.query.filter_by(name='User').first()
        if user_role is None:
            # This is a fallback in case roles aren't seeded.
            flash('Default user role not found. Please contact an administrator.', 'danger')
            return redirect(url_for('main.register'))

        user = User(username=form.username.data, email=form.email.data, role=user_role)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('main.login'))
        
    return render_template('register.html', title='Register', form=form)

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """Analytics page accessible only by admins."""
    # Query all login events, ordered by most recent
    events = LoginEvent.query.order_by(LoginEvent.timestamp.desc()).all()
    return render_template('analytics.html', events=events)