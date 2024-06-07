from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import User, db, Student
from sqlalchemy.exc import SQLAlchemyError

user_routes = Blueprint('users', __name__)


@user_routes.route('')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


# @user_routes.route('/<int:id>')
# @login_required
# def user(id):
#     """
#     Query for a user by id and returns that user in a dictionary
#     """
#     user = User.query.get(id)
#     return user.to_dict()

#  Update the status of the logged-in user to "Applied"

@user_routes.route('/update_status/applied', methods=['PUT'])
@login_required
def update_status_to_applied():
    try:
        # Assuming current_user gives you the user object of the logged-in user
        user = User.query.get(current_user.id)
        if user:
            user.status = "Applied"
            db.session.commit()
            return jsonify(user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

#   Update the status of a user by id

@user_routes.route('/<int:user_id>/update-status', methods=['PUT'])
@login_required
def update_user_status(user_id):
    if not current_user.is_parent():
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json()
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'Missing status'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.status = new_status
    try:
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': 'Could not update user status', 'details': str(e)}), 500

@user_routes.route('/all', methods=['GET'])
@login_required
def get_all_users():
    if not current_user.is_parent():
        return jsonify({"error": "Unauthorized access"}), 403

    users = User.query.all()
    users_list = []
    for user in users:
        user_data = {
            "email": user.email,
            "username": user.username,
            "status": user.status,
            "type": user.type,
            "created_date": user.created_date,
            "profile_link": f"/user/{user.id}",  # Assuming profile link is structured like this
        }

        # Fetch student information if exists
        student = Student.query.filter_by(user_id=user.id).first()
        if student:
            student_data = student.to_dict()
            # Extract and include only the relevant student information
            user_data.update({
                "student": {
                    "first_name": student_data["first_name"],
                    "last_name": student_data["last_name"],
                    "stage_name": student_data["stage_name"],
                    "profile_pic": student_data["profile_pic"],
                    "bio": student_data["bio"],
                    "phone": student_data["phone"],
                    "address_1": student_data["address_1"],
                    "address_2": student_data["address_2"],
                    "city": student_data["city"],
                    "state": student_data["state"],
                    "postal_code": student_data["postal_code"],
                    "portfolio_url": student_data["portfolio_url"],
                    "previous_projects": student_data["previous_projects"],
                    "instagram": student_data["instagram"],
                    "twitter": student_data["twitter"],
                    "facebook": student_data["facebook"],
                    "youtube": student_data["youtube"],
                    "other_social_media": student_data["other_social_media"],
                    "reference_name": student_data["reference_name"],
                    "reference_email": student_data["reference_email"],
                    "reference_phone": student_data["reference_phone"],
                    "reference_relationship": student_data["reference_relationship"],
                    "genres": student_data["genres"],
                    "types": student_data["types"]
                }
            })

        users_list.append(user_data)

    return jsonify(users_list)

#    Query for a user by id and returns that user in a dictionary, including student info if available
@user_routes.route('/<int:id>')
@login_required
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_dict = user.to_dict()

    # Check if the user has associated student information and include it
    student = Student.query.filter_by(user_id=id).first()
    if student:
        # If you have a to_dict method for Student, you can just call it
        student_dict = student.to_dict()
        user_dict["student"] = student_dict
    else:
        # Optionally handle the case where the user has no student information
        user_dict["student"] = "No student information available"

    return jsonify(user_dict), 200
