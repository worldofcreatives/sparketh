from flask import Blueprint, request, jsonify, render_template
from app.models import User, db, Student, Parent
from app.forms import LoginForm, StudentSignUpForm, ParentSignUpForm
from app.forms.password_reset_request_form import PasswordResetRequestForm
from app.forms.password_reset_form import PasswordResetForm
from flask_login import current_user, login_user, logout_user, login_required
from app.utils.email_utils import send_email, send_password_reset_email
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
from app.config import Config
import binascii
from werkzeug.security import generate_password_hash


auth_routes = Blueprint('auth', __name__)

s = URLSafeTimedSerializer(Config.SECRET_KEY)

SECRET_KEY = os.getenv('SECRET_KEY')

@auth_routes.route('')
def authenticate():
    """
    Authenticates a user.
    """
    if current_user.is_authenticated:
        return current_user.to_dict()
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        identifier = form.data['identifier']
        user = User.query.filter((User.email == identifier) | (User.username == identifier)).first()
        if user and user.check_password(form.data['password']):
            login_user(user)
            return user.to_dict()
        else:
            return {'errors': ['Invalid email/username or password.']}, 401
    return form.errors, 401

@auth_routes.route('/logout')
def logout():
    """
    Logs a user out
    """
    logout_user()
    return {'message': 'User logged out'}

# Sign up a parent

@auth_routes.route('/signup/parent', methods=['POST'])
def signup_parent():
    form = ParentSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        salt = binascii.hexlify(os.urandom(16)).decode()
        hashed_password = generate_password_hash(form.data['password'] + salt)
        user = User(
            username=form.data['username'],
            email=form.data['email'],
            hashed_password=hashed_password,
            salt=salt,
            type='parent',
            status='active'
        )
        db.session.add(user)
        db.session.commit()

        parent = Parent(user_id=user.id)
        db.session.add(parent)
        db.session.commit()

        return user.to_dict()
    return {'errors': form.errors}, 401

# Sign up a student, but you must be a parent to do so

@auth_routes.route('/signup/student', methods=['POST'])
@login_required
def signup_student():
    if not current_user.is_parent():
        return {'errors': 'Only parents can sign up students'}, 403

    form = StudentSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        salt = binascii.hexlify(os.urandom(16)).decode()
        hashed_password = generate_password_hash(form.data['password'] + salt)
        user = User(
            username=form.data['username'],
            email=None,
            hashed_password=hashed_password,
            salt=salt,
            type='student',
            status='active'
        )
        db.session.add(user)
        db.session.commit()

        student = Student(user_id=user.id, parent_id=current_user.id)
        db.session.add(student)
        db.session.commit()

        return user.to_dict()
    return {'errors': form.errors}, 401

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401
