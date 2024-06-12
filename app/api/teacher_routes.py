from flask import Blueprint, request, jsonify
from app.models import db, Teacher, User
from app.forms import TeacherSignUpForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

teacher_routes = Blueprint('teachers', __name__)

# Register a teacher

@teacher_routes.route('/register', methods=['POST'])
def register_teacher():
    form = TeacherSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
            type='teacher'
        )
        db.session.add(user)
        db.session.commit()

        teacher = Teacher(
            user_id=user.id,
            profile_pic=form.profile_pic.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            address_1=form.address_1.data,
            address_2=form.address_2.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            bio=form.bio.data,
            expertise=form.expertise.data
        )
        db.session.add(teacher)
        db.session.commit()
        login_user(user)
        return jsonify(teacher.to_dict()), 201
    return jsonify(form.errors), 400

# Login a teacher

@teacher_routes.route('/login', methods=['POST'])
def login_teacher():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data) and user.type == 'teacher':
            login_user(user)
            return jsonify(user.to_dict()), 200
    return jsonify({"error": "Invalid credentials"}), 400

# Get teacher profile

@teacher_routes.route('/profile', methods=['GET'])
@login_required
def get_teacher_profile():
    if current_user.type == 'teacher':
        teacher = Teacher.query.filter_by(user_id=current_user.id).first()
        if teacher:
            return jsonify(teacher.to_dict()), 200
    return jsonify({"error": "Unauthorized access"}), 401

# Update teacher profile

@teacher_routes.route('/profile', methods=['PUT'])
@login_required
def update_teacher_profile():
    if current_user.type == 'teacher':
        form = TeacherSignUpForm()
        if form.validate_on_submit():
            teacher = Teacher.query.filter_by(user_id=current_user.id).first()
            if teacher:
                teacher.profile_pic = form.profile_pic.data
                teacher.first_name = form.first_name.data
                teacher.last_name = form.last_name.data
                teacher.address_1 = form.address_1.data
                teacher.address_2 = form.address_2.data
                teacher.city = form.city.data
                teacher.state = form.state.data
                teacher.zip_code = form.zip_code.data
                teacher.bio = form.bio.data
                teacher.expertise = form.expertise.data
                db.session.commit()
                return jsonify(teacher.to_dict()), 200
        return jsonify(form.errors), 400
    return jsonify({"error": "Unauthorized access"}), 401

# Logout a teacher

@teacher_routes.route('/logout', methods=['POST'])
@login_required
def logout_teacher():
    if current_user.type == 'teacher':
        logout_user()
        return jsonify({"message": "Logged out successfully"}), 200
    return jsonify({"error": "Unauthorized access"}), 401

# GET all teachers

@teacher_routes.route('/', methods=['GET'])
def get_all_teachers():
    teachers = Teacher.query.all()
    return jsonify([teacher.to_dict() for teacher in teachers]), 200
