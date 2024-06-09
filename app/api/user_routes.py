from flask import Blueprint, request, jsonify
from app.models import db, User, Parent, Student
from app.forms import LoginForm, ParentSignUpForm, StudentSignUpForm, ParentProfileForm, StudentProfileForm
from datetime import date
from flask_login import login_user, logout_user, current_user, login_required

user_routes = Blueprint('users', __name__)

# Register a new user as a parent
@user_routes.route('/register', methods=['POST'])
def register():
    form = ParentSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            type='parent'
        )
        db.session.add(new_user)
        db.session.commit()
        new_parent = Parent(user_id=new_user.id)
        db.session.add(new_parent)
        db.session.commit()

        # Log the user in
        login_user(new_user)

        return jsonify(new_user.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Parents can register their kids
@user_routes.route('/parent/<int:parent_id>/register-kid', methods=['POST'])
@login_required
def register_kid(parent_id):
    form = StudentSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    parent = Parent.query.get_or_404(parent_id)

    # Check if the current user is an admin or the parent
    if current_user.type != 'admin' and current_user.id != parent.user_id:
        return jsonify({'errors': 'Unauthorized access'}), 403

    if form.validate_on_submit():
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            type='student'
        )
        db.session.add(new_user)
        db.session.commit()
        new_student = Student(
            user_id=new_user.id,
            parent_id=parent_id,
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    return jsonify({'errors': form.errors}), 400


# Parent login, and only works with parent accounts
@user_routes.route('/login/parent', methods=['POST'])
def login_parent():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.identifier.data) | (User.username == form.identifier.data)).first()
        if user and user.type == 'parent' and user.check_password(form.data['password']):
            login_user(user)
            return jsonify(user.to_dict())
        else:
            return jsonify({'errors': ['Invalid email/username or password, or not a parent account.']}), 401
    return jsonify({'errors': form.errors}), 400

# Student login, and only works with student accounts
@user_routes.route('/login/student', methods=['POST'])
def login_student():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.identifier.data).first()
        if user and user.type == 'student' and user.check_password(form.data['password']):
            login_user(user)
            return jsonify(user.to_dict())
        else:
            return jsonify({'errors': ['Invalid username or password, or not a student account.']}), 401
    return jsonify({'errors': form.errors}), 400

# Parents can update profile info (only for the data in the payload)
@user_routes.route('/parent/<int:parent_id>/profile', methods=['POST'])
@login_required
def update_parent_profile(parent_id):
    form = ParentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    parent = Parent.query.get_or_404(parent_id)

    # Check if the current user is an admin or the parent
    if current_user.type != 'admin' and current_user.id != parent.user_id:
        return jsonify({'errors': 'Unauthorized access'}), 403

    if form.validate_on_submit():
        # Update only the fields sent in the form
        if form.profile_pic.data:
            parent.profile_pic = form.profile_pic.data
        if form.first_name.data:
            parent.first_name = form.first_name.data
        if form.last_name.data:
            parent.last_name = form.last_name.data
        if form.address_1.data:
            parent.address_1 = form.address_1.data
        if form.address_2.data:
            parent.address_2 = form.address_2.data
        if form.city.data:
            parent.city = form.city.data
        if form.state.data:
            parent.state = form.state.data
        if form.zip_code.data:
            parent.zip_code = form.zip_code.data
        if form.stripe_customer_id.data:
            parent.stripe_customer_id = form.stripe_customer_id.data
        if form.stripe_subscription_id.data:
            parent.stripe_subscription_id = form.stripe_subscription_id.data

        db.session.commit()
        return jsonify(parent.to_dict()), 200

    return jsonify({'errors': form.errors}), 400


# Students or their parent can update the student's profile info
@user_routes.route('/student/<int:student_id>/profile', methods=['POST'])
@login_required
def add_student_profile(student_id):
    form = StudentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    # Fetch the student record
    student = Student.query.get_or_404(student_id)
    parent = Parent.query.get_or_404(student.parent_id)

    # Check if the current user is an admin, the student themselves, or the parent of the student
    if not (current_user.type == 'admin' or current_user.id == student.user_id or current_user.id == parent.user_id):
        return jsonify({'errors': 'Unauthorized access'}), 403

    if form.validate_on_submit():
        if form.bio.data:
            student.bio = form.bio.data
        if form.date_of_birth.data:
            # Assuming the date_of_birth data is a string in 'YYYY-MM-DD' format
            year, month, day = map(int, form.date_of_birth.data.split('-'))
            student.date_of_birth = date(year, month, day)
        if form.skill_level.data:
            student.skill_level = form.skill_level.data
        if form.progress.data:
            student.progress = form.progress.data

        db.session.commit()
        return jsonify(student.to_dict()), 200

    return jsonify({'errors': form.errors}), 400


# ------------- Other routes, not tested ---------------

# When a parent's status is set to "active" their kid's accounts status is set to "active"
@user_routes.route('/parent/<int:parent_id>/status/active', methods=['PUT'])
def activate_parent_and_kids(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    parent.user.status = 'active'
    for student in parent.students:
        student.user.status = 'active'
    db.session.commit()
    return jsonify({'parent_status': 'active', 'students_status': 'active'}), 200

# When a parent's status is set to "inactive" their kid's accounts status is set to "inactive"
@user_routes.route('/parent/<int:parent_id>/status/inactive', methods=['PUT'])
def deactivate_parent_and_kids(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    parent.user.status = 'inactive'
    for student in parent.students:
        student.user.status = 'inactive'
    db.session.commit()
    return jsonify({'parent_status': 'inactive', 'students_status': 'inactive'}), 200

# A route that gets the current user's profile information
@user_routes.route('/profile', methods=['GET'])
def get_profile():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    return jsonify({'errors': 'Not authenticated'}), 401
