# routes/track_routes.py
from flask import Blueprint, request, jsonify
from app.models import db, Track, Course, Student, Teacher, track_course_table
from ..api.aws_helpers import get_unique_filename, upload_file_to_s3
from .helper_functions import is_allowed_file

from flask_login import current_user, login_required
from datetime import datetime

track_routes = Blueprint('tracks', __name__)

# Create a new track
@track_routes.route('', methods=['POST'])
@login_required
def create_track():
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can create tracks'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    objectives = data.get('objectives', '')
    outcomes = data.get('outcomes', '')

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    new_track = Track(
        title=title,
        description=description,
        objectives=objectives,
        outcomes=outcomes,
        teacher_id=teacher.id
    )
    db.session.add(new_track)
    db.session.commit()

    return jsonify(new_track.to_dict()), 201

# Add a course to a track
@track_routes.route('/<int:track_id>/courses/<int:course_id>', methods=['POST'])
@login_required
def add_course_to_track(track_id, course_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can add courses to tracks'}), 403

    track = Track.query.get(track_id)
    if not track:
        return jsonify({'errors': 'Track not found'}), 404

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    if track.teacher_id != teacher.id:
        return jsonify({'errors': 'You are not the creator of this track'}), 403

    course = Course.query.get(course_id)
    if not course:
        return jsonify({'errors': 'Course not found'}), 404

    # Check if the course is already in the track
    existing_entry = db.session.query(track_course_table).filter_by(track_id=track_id, course_id=course_id).first()
    if existing_entry:
        return jsonify({'errors': 'Course already in track'}), 400

    order = len(track.courses) + 1
    db.session.execute(track_course_table.insert().values(track_id=track_id, course_id=course_id, order=order))
    db.session.commit()

    return jsonify(track.to_dict()), 200

# Reorder courses in a track
@track_routes.route('/<int:track_id>/reorder_courses', methods=['PUT'])
@login_required
def reorder_courses_in_track(track_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can reorder courses in tracks'}), 403

    track = Track.query.get(track_id)
    if not track:
        return jsonify({'errors': 'Track not found'}), 404

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    if track.teacher_id != teacher.id:
        return jsonify({'errors': 'You are not the creator of this track'}), 403

    data = request.get_json()
    new_order = data.get('order')  # Expects a list of course IDs in the new order

    for index, course_id in enumerate(new_order):
        db.session.execute(track_course_table.update().where(
            track_course_table.c.track_id == track_id,
            track_course_table.c.course_id == course_id
        ).values(order=index + 1))

    db.session.commit()

    return jsonify(track.to_dict()), 200

# Remove a course from a track
@track_routes.route('/<int:track_id>/courses/<int:course_id>', methods=['DELETE'])
@login_required
def remove_course_from_track(track_id, course_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can remove courses from tracks'}), 403

    track = Track.query.get(track_id)
    if not track:
        return jsonify({'errors': 'Track not found'}), 404

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    if track.teacher_id != teacher.id:
        return jsonify({'errors': 'You are not the creator of this track'}), 403

    # Check if the course is in the track
    course_in_track = db.session.query(track_course_table).filter_by(track_id=track_id, course_id=course_id).first()
    if not course_in_track:
        return jsonify({'errors': 'Course not in track'}), 404

    # Remove the course from the track
    db.session.execute(track_course_table.delete().where(
        track_course_table.c.track_id == track_id,
        track_course_table.c.course_id == course_id
    ))
    db.session.commit()

    # Ensure the courses are returned in the correct order
    updated_track = Track.query.get(track_id)
    return jsonify(updated_track.to_dict()), 200

# Student joins a track
@track_routes.route('/<int:track_id>/join', methods=['POST'])
@login_required
def join_track(track_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can join tracks'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    track = Track.query.get(track_id)

    if not student or not track:
        return jsonify({'errors': 'Student or Track not found'}), 404

    student.joined_tracks.append(track)
    db.session.commit()
    return jsonify(student.to_dict()), 200

# Student withdraws a track
@track_routes.route('/<int:track_id>/withdraw', methods=['POST'])
@login_required
def withdraw_track(track_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can withdraw tracks'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    track = Track.query.get(track_id)

    if not student or not track:
        return jsonify({'errors': 'Student or Track not found'}), 404

    # Check if the track exists in the student's joined tracks
    if track in student.joined_tracks:
        student.joined_tracks.remove(track)
        db.session.commit()
        return jsonify(student.to_dict()), 200
    else:
        return jsonify({'errors': 'Track not found in student\'s joined tracks'}), 404

# Get all tracks
@track_routes.route('', methods=['GET'])
@login_required
def get_all_tracks():
    tracks = Track.query.all()
    return jsonify([track.to_dict() for track in tracks]), 200

# Get a specific track
@track_routes.route('/<int:track_id>', methods=['GET'])
@login_required
def get_track(track_id):
    track = Track.query.get(track_id)
    if not track:
        return jsonify({'errors': 'Track not found'}), 404

    return jsonify(track.to_dict()), 200

# Upload downloadable files for a track
@track_routes.route('/<int:track_id>/files', methods=['POST'])
@login_required
def upload_files_for_track(track_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can upload files for tracks'}), 403

    track = Track.query.get(track_id)
    if not track:
        return jsonify({'errors': 'Track not found'}), 404

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    if track.teacher_id != teacher.id:
        return jsonify({'errors': 'You are not the creator of this track'}), 403

    files = request.files.getlist('files')
    file_urls = []

    for file in files:
        if file and is_allowed_file(file.filename, {"pdf", "doc", "docx", "ppt", "pptx"}):
            file_name = get_unique_filename(file.filename)
            file_url_response = upload_file_to_s3(file, file_name)

            if "url" in file_url_response:
                file_urls.append(file_url_response["url"])
            else:
                error_message = file_url_response.get("errors", "Unknown error during file upload.")
                return jsonify({"errors": f"File upload failed: {error_message}"}), 500

    if not track.downloadable_files:
        track.downloadable_files = []

    track.downloadable_files.extend(file_urls)
    db.session.commit()

    return jsonify(track.to_dict()), 200
