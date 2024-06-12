from flask import Blueprint, request, jsonify
from app.models import db, Art, Student, Teacher
from app.forms import ArtForm
from flask_login import current_user, login_required
from ..api.aws_helpers import get_unique_filename, upload_file_to_s3
import os
from .helper_functions import award_points
from datetime import datetime

art_routes = Blueprint('art', __name__)

# Helper functions
def is_allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB in bytes

def file_size_under_limit(file):
    file.seek(0, os.SEEK_END)  # Go to the end of the file
    file_size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return file_size <= MAX_FILE_SIZE

# ------- UPLOADING ART -------

# Upload art
# @art_routes.route('', methods=['POST'])
# @login_required
# def upload_art():

#     if current_user.type != 'student':
#         return jsonify({'errors': 'Only students can upload art'}), 403

#     # Find the student record associated with the current user
#     student = Student.query.filter_by(user_id=current_user.id).first()
#     if not student:
#         return jsonify({'errors': 'Student not found'}), 404

#     form = ArtForm()
#     form['csrf_token'].data = request.cookies['csrf_token']
#     form.user_id.data = student.user_id


#     if form.validate_on_submit():
#         file = request.files.get('file')

#         # Check both file type and file size
#         if file and is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}) and file_size_under_limit(file):
#             file_name = get_unique_filename(file.filename)
#             file_url_response = upload_file_to_s3(file, file_name)

#             if "url" in file_url_response:
#                 new_art = Art(
#                     name=form.name.data,
#                     type=form.type.data,
#                     user_id=student.id,
#                     course_id=form.course_id.data,
#                     media_url=file_url_response["url"]
#                 )
#                 db.session.add(new_art)
#                 db.session.commit()
#                 # Award points for uploading art
#                 award_points(student, 20)
#                 return jsonify(new_art.to_dict()), 201
#             else:
#                 error_message = file_url_response.get("errors", "Unknown error during file upload.")
#                 return jsonify({"errors": f"File upload failed: {error_message}"}), 500
#         else:
#             # Return an appropriate error message if the file type is not allowed or file size exceeds the limit
#             if not is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}):
#                 return jsonify({"error": "File type not allowed"}), 400
#             if not file_size_under_limit(file):
#                 return jsonify({"error": "File size exceeds limit"}), 400

#     return jsonify({'errors': form.errors}), 400

@art_routes.route('', methods=['POST'])
@login_required
def upload_art():
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can upload art'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        return jsonify({'errors': 'Student not found'}), 404

    form = ArtForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    form.user_id.data = student.user_id

    if form.validate_on_submit():
        file = request.files.get('file')
        if file and is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}) and file_size_under_limit(file):
            file_name = get_unique_filename(file.filename)
            file_url_response = upload_file_to_s3(file, file_name)

            if "url" in file_url_response:
                new_art = Art(
                    name=form.name.data,
                    type=form.type.data,
                    user_id=student.id,
                    course_id=form.course_id.data,
                    media_url=file_url_response["url"],
                    public=form.public.data if 'public' in form else True,
                    open_to_feedback=form.open_to_feedback.data if 'open_to_feedback' in form else False
                )
                db.session.add(new_art)
                db.session.commit()
                award_points(student, 20)
                return jsonify(new_art.to_dict()), 201
            else:
                error_message = file_url_response.get("errors", "Unknown error during file upload.")
                return jsonify({"errors": f"File upload failed: {error_message}"}), 500
        else:
            if not is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}):
                return jsonify({"error": "File type not allowed"}), 400
            if not file_size_under_limit(file):
                return jsonify({"error": "File size exceeds limit"}), 400

    return jsonify({'errors': form.errors}), 400

# ------- GETTING ALL THE ART IN VARIOUS WAYS -------

# Get all art
@art_routes.route('/', methods=['GET'])
def get_all_art():
    artworks = Art.query.all()
    return jsonify([art.to_dict() for art in artworks])

# Get all art based on user
@art_routes.route('/user/<int:user_id>', methods=['GET'])
def get_art_by_user(user_id):
    artworks = Art.query.filter_by(user_id=user_id).all()
    return jsonify([art.to_dict() for art in artworks])

# Get all art based on course
@art_routes.route('/course/<int:course_id>', methods=['GET'])
def get_art_by_course(course_id):
    artworks = Art.query.filter_by(course_id=course_id).all()
    return jsonify([art.to_dict() for art in artworks])

#------- FEEDBACK ON ART -------

# Submit feedback
@art_routes.route('/<int:art_id>/feedback', methods=['POST'])
@login_required
def submit_feedback(art_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can submit feedback'}), 403

    art = Art.query.get(art_id)
    if not art:
        return jsonify({'errors': 'Art not found'}), 404

    if not art.open_to_feedback:
        return jsonify({'errors': 'Art is not open to feedback'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    feedback_data = request.get_json()
    feedback = {
        "teacher_id": teacher.id,
        "teacher_name": f"{teacher.first_name} {teacher.last_name}",
        "feedback": feedback_data.get('feedback', ''),
        "date": datetime.utcnow().isoformat()
    }
    art.feedback.append(feedback)
    art.open_to_feedback = False  # Close feedback once provided
    db.session.commit()

    return jsonify(art.to_dict()), 200

# Get all art open to feedback
@art_routes.route('/open_to_feedback', methods=['GET'])
@login_required
def get_open_to_feedback_art():
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can view this list'}), 403

    artworks = Art.query.filter_by(open_to_feedback=True).all()
    return jsonify([art.to_dict() for art in artworks]), 200

# Get all art open to feedback in a speciifc course
@art_routes.route('/open_to_feedback/course/<int:course_id>', methods=['GET'])
@login_required
def get_open_to_feedback_art_by_course(course_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can view this list'}), 403

    artworks = Art.query.filter_by(course_id=course_id, open_to_feedback=True).all()
    return jsonify([art.to_dict() for art in artworks]), 200

# Get all art that has not received feedback yet
@art_routes.route('/no_feedback', methods=['GET'])
@login_required
def get_no_feedback_art():
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can view this list'}), 403

    artworks = Art.query.filter(Art.open_to_feedback == True, Art.feedback == []).all()
    return jsonify([art.to_dict() for art in artworks]), 200

# Get all art that has not received feedback yet in a specific course
@art_routes.route('/no_feedback/course/<int:course_id>', methods=['GET'])
@login_required
def get_no_feedback_art_by_course(course_id):
    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can view this list'}), 403

    artworks = Art.query.filter(Art.course_id == course_id, Art.open_to_feedback == True, Art.feedback == []).all()
    return jsonify([art.to_dict() for art in artworks]), 200

# ------- DELETING ART -------

# Delete art
@art_routes.route('/<int:art_id>', methods=['DELETE'])
@login_required
def delete_art(art_id):
    art = Art.query.get(art_id)
    if not art:
        return jsonify({'errors': 'Art not found'}), 404

    if current_user.id != art.user_id:
        return jsonify({'errors': 'You do not have permission to delete this art'}), 403

    db.session.delete(art)
    db.session.commit()
    return jsonify({'message': 'Art deleted successfully'}), 200
