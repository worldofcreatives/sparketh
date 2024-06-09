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
            type='Parent',
            status='Accepted'
        )
        db.session.add(user)
        db.session.commit()

        parent = Parent(user_id=user.id, name=user.username)
        db.session.add(parent)
        db.session.commit()

        return user.to_dict()
    return {'errors': form.errors}, 401

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
            type='Student',
            status='Pre-Apply'
        )
        db.session.add(user)
        db.session.commit()

        student = Student(user_id=user.id, parent_id=current_user.parent.id)
        db.session.add(student)
        db.session.commit()

        return user.to_dict()
    return {'errors': form.errors}, 401

@auth_routes.route('/update_status', methods=['PUT'])
@login_required
def update_status():
    """
    Updates the current user's status to 'Applied'.
    """
    if current_user.status == 'Pre-Apply':
        current_user.status = 'Applied'
        db.session.commit()
        return {'status': 'Updated', 'user': current_user.to_dict()}
    return {'status': 'No Change', 'user': current_user.to_dict()}

@auth_routes.route('/update_status/<int:user_id>', methods=['PUT'])
@login_required
def update_user_status(user_id):
    """
    Updates the specified user's status to 'Accepted' or 'Denied'.
    Only accessible by users with the type 'Parent'.
    """
    if current_user.type != 'Parent':
        return {'errors': ['Unauthorized. Only parents can perform this action.']}, 403

    data = request.get_json()
    status = data.get('status')
    if status not in ['Accepted', 'Denied', 'Applied', 'Pre-Apply', 'Premium Monthly', 'Premium Annual']:
        return {'errors': ['Invalid status.']}, 400

    user = User.query.get(user_id)
    if not user:
        return {'errors': ['User not found.']}, 404

    user.status = status
    db.session.commit()
    return {'status': 'Updated', 'user': user.to_dict()}

@auth_routes.route('/unauthorized')
def unauthorized():
    """
    Returns unauthorized JSON when flask-login authentication fails
    """
    return {'errors': {'message': 'Unauthorized'}}, 401

@auth_routes.route('/password_reset_request', methods=['POST'])
def password_reset_request():
    """
    Sends a password reset email to the user.
    """
    form = PasswordResetRequestForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.data['email']).first()
        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_url = f"{request.host_url}reset_password/{token}"
            send_email(user.email, 'Password Reset Request', f'Click the link to reset your password: {reset_url}')
        return {'message': 'If an account with that email exists, a password reset email has been sent.'}, 200
    return jsonify({'errors': form.errors}), 401

@auth_routes.route('/reset_password/<token>', methods=['POST'])
def reset_password(token):
    """
    Resets the user's password using the token.
    """
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except SignatureExpired:
        return {'errors': {'message': 'The token is expired.'}}, 400

    form = PasswordResetForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = form.data['password']
            db.session.commit()
            return {'message': 'Your password has been reset successfully.'}, 200
    return jsonify({'errors': form.errors}), 401
