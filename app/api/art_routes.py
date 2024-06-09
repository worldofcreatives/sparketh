from flask import Blueprint, request, jsonify
from app.models import db, Art
from app.forms import ArtForm
from ..api.aws_helpers import get_unique_filename, upload_file_to_s3
import os

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

# Upload art
@art_routes.route('/', methods=['POST'])
def upload_art():
    form = ArtForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        file = request.files.get('file')

        # Check both file type and file size
        if file and is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}) and file_size_under_limit(file):
            file_name = get_unique_filename(file.filename)
            file_url_response = upload_file_to_s3(file, file_name)

            if "url" in file_url_response:
                new_art = Art(
                    name=form.name.data,
                    type=form.type.data,
                    user_id=form.user_id.data,
                    course_id=form.course_id.data,
                    media_url=file_url_response["url"]
                )
                db.session.add(new_art)
                db.session.commit()
                return jsonify(new_art.to_dict()), 201
            else:
                error_message = file_url_response.get("errors", "Unknown error during file upload.")
                return jsonify({"errors": f"File upload failed: {error_message}"}), 500
        else:
            # Return an appropriate error message if the file type is not allowed or file size exceeds the limit
            if not is_allowed_file(file.filename, {"jpg", "jpeg", "png", "gif"}):
                return jsonify({"error": "File type not allowed"}), 400
            if not file_size_under_limit(file):
                return jsonify({"error": "File size exceeds limit"}), 400

    return jsonify({'errors': form.errors}), 400

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


# from flask import Blueprint, request, jsonify
# from app.models import db, Art
# from app.forms import ArtForm

# art_routes = Blueprint('art', __name__)

# # Upload art
# @art_routes.route('/', methods=['POST'])
# def upload_art():
#     form = ArtForm()
#     if form.validate_on_submit():
#         new_art = Art(
#             name=form.name.data,
#             type=form.type.data,
#             user_id=form.user_id.data,
#             course_id=form.course_id.data,
#             media_url=form.media_url.data
#         )
#         db.session.add(new_art)
#         db.session.commit()
#         return jsonify(new_art.to_dict()), 201
#     return jsonify({'errors': form.errors}), 400

# # Get all art
# @art_routes.route('/', methods=['GET'])
# def get_all_art():
#     artworks = Art.query.all()
#     return jsonify([art.to_dict() for art in artworks])

# # Get all art based on user
# @art_routes.route('/user/<int:user_id>', methods=['GET'])
# def get_art_by_user(user_id):
#     artworks = Art.query.filter_by(user_id=user_id).all()
#     return jsonify([art.to_dict() for art in artworks])

# # Get all art based on course
# @art_routes.route('/course/<int:course_id>', methods=['GET'])
# def get_art_by_course(course_id):
#     artworks = Art.query.filter_by(course_id=course_id).all()
#     return jsonify([art.to_dict() for art in artworks])
