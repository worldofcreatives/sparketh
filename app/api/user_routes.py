from flask import Blueprint, request, jsonify
from app.models import db, User, Parent, Student
from app.forms import LoginForm, ParentSignUpForm, StudentSignUpForm, ParentProfileForm, StudentProfileForm
from flask_login import login_user, logout_user, current_user

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
        return jsonify(new_user.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Parents can register their kids
@user_routes.route('/parent/<int:parent_id>/register-kid', methods=['POST'])
def register_kid(parent_id):
    form = StudentSignUpForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        parent = Parent.query.get_or_404(parent_id)
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            type='student'
        )
        db.session.add(new_user)
        db.session.commit()
        new_child = Student(
            user_id=new_user.id,
            parent_id=parent_id,
        )
        db.session.add(new_child)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Parent login
@user_routes.route('/login/parent', methods=['POST'])
def login_parent():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.identifier.data) | (User.username == form.identifier.data)).first()
        login_user(user)
        return jsonify(user.to_dict())
    return jsonify({'errors': form.errors}), 400

# Student login
@user_routes.route('/login/student', methods=['POST'])
def login_student():
    form = LoginForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.identifier.data).first()
        login_user(user)
        return jsonify(user.to_dict())
    return jsonify({'errors': form.errors}), 400

# Parents can add profile info
@user_routes.route('/parent/<int:parent_id>/profile', methods=['POST'])
def add_parent_profile(parent_id):
    form = ParentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        parent = Parent.query.get_or_404(parent_id)
        parent.profile_pic = form.profile_pic.data
        parent.first_name = form.first_name.data
        parent.last_name = form.last_name.data
        parent.address_1 = form.address_1.data
        parent.address_2 = form.address_2.data
        parent.city = form.city.data
        parent.state = form.state.data
        parent.zip_code = form.zip_code.data
        parent.stripe_customer_id = form.stripe_customer_id.data
        parent.stripe_subscription_id = form.stripe_subscription_id.data
        db.session.commit()
        return jsonify(parent.to_dict())
    return jsonify({'errors': form.errors}), 400

# Parents can update profile info
@user_routes.route('/parent/<int:parent_id>/profile', methods=['PUT'])
def update_parent_profile(parent_id):
    form = ParentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        parent = Parent.query.get_or_404(parent_id)
        parent.profile_pic = form.profile_pic.data
        parent.first_name = form.first_name.data
        parent.last_name = form.last_name.data
        parent.address_1 = form.address_1.data
        parent.address_2 = form.address_2.data
        parent.city = form.city.data
        parent.state = form.state.data
        parent.zip_code = form.zip_code.data
        parent.stripe_customer_id = form.stripe_customer_id.data
        parent.stripe_subscription_id = form.stripe_subscription_id.data
        db.session.commit()
        return jsonify(parent.to_dict())
    return jsonify({'errors': form.errors}), 400

# Students can add profile info
@user_routes.route('/student/<int:student_id>/profile', methods=['POST'])
def add_student_profile(student_id):
    form = StudentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        student = Student.query.get_or_404(student_id)
        student.name = form.name.data
        student.date_of_birth = form.date_of_birth.data
        student.skill_level = form.skill_level.data
        student.progress = form.progress.data
        db.session.commit()
        return jsonify(student.to_dict())
    return jsonify({'errors': form.errors}), 400

# Students can update profile info
@user_routes.route('/student/<int:student_id>/profile', methods=['PUT'])
def update_student_profile(student_id):
    form = StudentProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        student = Student.query.get_or_404(student_id)
        student.name = form.name.data
        student.date_of_birth = form.date_of_birth.data
        student.skill_level = form.skill_level.data
        student.progress = form.progress.data
        db.session.commit()
        return jsonify(student.to_dict())
    return jsonify({'errors': form.errors}), 400

# When a parent's status is set to "active" their kid's accounts status is set to "active"
@user_routes.route('/parent/<int:parent_id>/status/active', methods=['PUT'])
def activate_parent_and_kids(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    parent.user.status = 'active'
    for child in parent.children:
        child.user.status = 'active'
    db.session.commit()
    return jsonify({'parent_status': 'active', 'children_status': 'active'}), 200

# When a parent's status is set to "inactive" their kid's accounts status is set to "inactive"
@user_routes.route('/parent/<int:parent_id>/status/inactive', methods=['PUT'])
def deactivate_parent_and_kids(parent_id):
    parent = Parent.query.get_or_404(parent_id)
    parent.user.status = 'inactive'
    for child in parent.children:
        child.user.status = 'inactive'
    db.session.commit()
    return jsonify({'parent_status': 'inactive', 'children_status': 'inactive'}), 200

# A route that gets the current user's profile information
@user_routes.route('/profile', methods=['GET'])
def get_profile():
    if current_user.is_authenticated:
        return jsonify(current_user.to_dict())
    return jsonify({'errors': 'Not authenticated'}), 401
