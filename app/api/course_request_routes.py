# routes/course_request_routes.py
from flask import Blueprint, request, jsonify
from app.models import db, CourseRequest, Student, Teacher
from flask_login import current_user, login_required
from datetime import datetime

course_request_routes = Blueprint('course_requests', __name__)

# Request a new course
@course_request_routes.route('', methods=['POST'])
@login_required
def request_course():
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can request courses'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        return jsonify({'errors': 'Student not found'}), 404

    new_request = CourseRequest(
        title=title,
        description=description,
        requested_by=student.id
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify(new_request.to_dict()), 201

# Upvote a course request
@course_request_routes.route('/<int:request_id>/upvote', methods=['POST'])
@login_required
def upvote_course_request(request_id):
    course_request = CourseRequest.query.get(request_id)
    if not course_request:
        return jsonify({'errors': 'Course request not found'}), 404

    course_request.upvotes += 1
    db.session.commit()

    return jsonify(course_request.to_dict()), 200

# Downvote a course request
@course_request_routes.route('/<int:request_id>/downvote', methods=['POST'])
@login_required
def downvote_course_request(request_id):
    course_request = CourseRequest.query.get(request_id)
    if not course_request:
        return jsonify({'errors': 'Course request not found'}), 404

    course_request.downvotes += 1
    db.session.commit()

    return jsonify(course_request.to_dict()), 200

# Teacher opts to work on a course request
@course_request_routes.route('/<int:request_id>/opt_in', methods=['POST'])
@login_required
def opt_in_course_request(request_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can opt-in to work on courses'}), 403

    course_request = CourseRequest.query.get(request_id)
    if not course_request:
        return jsonify({'errors': 'Course request not found'}), 404

    if course_request.opted_by:
        return jsonify({'errors': 'Course request already opted in by another teacher'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course_request.opted_by = teacher.id
    course_request.status = 'working on'
    db.session.commit()

    return jsonify(course_request.to_dict()), 200

# Update course request status
@course_request_routes.route('/<int:request_id>/status', methods=['PUT'])
@login_required
def update_course_status(request_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can update the course status'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course_request = CourseRequest.query.get(request_id)
    if not course_request:
        return jsonify({'errors': 'Course request not found'}), 404

    if course_request.opted_by != teacher.id:
        return jsonify({'errors': 'You have not opted in to work on this course'}), 403

    data = request.get_json()
    status = data.get('status')

    if status not in ['idle', 'working on', 'launched']:
        return jsonify({'errors': 'Invalid status'}), 400

    course_request.status = status
    course_request.updated_date = datetime.utcnow()
    db.session.commit()

    return jsonify(course_request.to_dict()), 200

# Teacher opts out of working on a course request
@course_request_routes.route('/<int:request_id>/opt_out', methods=['POST'])
@login_required
def opt_out_course_request(request_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can opt-out of working on courses'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course_request = CourseRequest.query.get(request_id)
    if not course_request:
        return jsonify({'errors': 'Course request not found'}), 404

    if course_request.opted_by != teacher.id:
        return jsonify({'errors': 'You have not opted in to work on this course'}), 403

    course_request.opted_by = None
    course_request.status = 'idle'
    db.session.commit()

    return jsonify(course_request.to_dict()), 200

# Get all course requests
@course_request_routes.route('', methods=['GET'])
@login_required
def get_all_course_requests():
    course_requests = CourseRequest.query.all()
    return jsonify([request.to_dict() for request in course_requests]), 200
