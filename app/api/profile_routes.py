from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, User, Parent, Student, Genre, Type
from app.forms.profile_form import ProfileForm
from werkzeug.utils import secure_filename
import os
import logging
from sqlalchemy.exc import IntegrityError
from ..api.aws_helpers import get_unique_filename, upload_file_to_s3

profile_routes = Blueprint('profiles', __name__)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB in bytes

def is_allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

def file_size_under_limit(file):
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer to the beginning
    return file_size <= MAX_FILE_SIZE

@profile_routes.route('/', methods=['POST', 'PUT'])
@login_required
def update_profile():
    user = current_user
    form = ProfileForm()
    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():
        # Handle Student profile picture upload
        if user.type == 'Student' and 'profile_pic' in request.files:
            profile_pic = request.files['profile_pic']
            if profile_pic and is_allowed_file(profile_pic.filename, {'jpg', 'jpeg', 'png', 'gif'}) and file_size_under_limit(profile_pic):
                file_name = get_unique_filename(profile_pic.filename)
                file_url_response = upload_file_to_s3(profile_pic, file_name)
                if "url" in file_url_response:
                    student = Student.query.filter_by(user_id=user.id).first()
                    student.profile_pic = file_url_response["url"]
                else:
                    return jsonify({"errors": "Failed to upload profile picture"}), 500
            else:
                return jsonify({"errors": "Invalid file or file size exceeds limit."}), 400

        # Handle Parent logo upload
        if user.type == 'Parent' and 'logo' in request.files:
            logo = request.files['logo']
            if logo and is_allowed_file(logo.filename, {'jpg', 'jpeg', 'png', 'gif'}) and file_size_under_limit(logo):
                file_name = get_unique_filename(logo.filename)
                file_url_response = upload_file_to_s3(logo, file_name)
                if "url" in file_url_response:
                    parent = Parent.query.filter_by(user_id=user.id).first()
                    parent.logo = file_url_response["url"]
                else:
                    return jsonify({"errors": "Failed to upload parent logo"}), 500
            else:
                return jsonify({"errors": "Invalid file or file size exceeds limit."}), 400

        if user.type == 'Student':
            student = Student.query.filter_by(user_id=user.id).first()

            student.first_name = form.first_name.data if form.first_name.data else student.first_name
            student.last_name = form.last_name.data if form.last_name.data else student.last_name
            student.stage_name = form.stage_name.data if form.stage_name.data else student.stage_name
            student.bio = form.bio.data if form.bio.data else student.bio
            student.phone = form.phone.data if form.phone.data else student.phone
            student.address_1 = form.address_1.data if form.address_1.data else student.address_1
            student.address_2 = form.address_2.data if form.address_2.data else student.address_2
            student.city = form.city.data if form.city.data else student.city
            student.state = form.state.data if form.state.data else student.state
            student.postal_code = form.postal_code.data if form.postal_code.data else student.postal_code
            student.portfolio_url = form.portfolio_url.data if form.portfolio_url.data else student.portfolio_url
            student.previous_projects = form.previous_projects.data if form.previous_projects.data else student.previous_projects
            student.instagram = form.instagram.data if form.instagram.data else student.instagram
            student.twitter = form.twitter.data if form.twitter.data else student.twitter
            student.facebook = form.facebook.data if form.facebook.data else student.facebook
            student.youtube = form.youtube.data if form.youtube.data else student.youtube
            student.other_social_media = form.other_social_media.data if form.other_social_media.data else student.other_social_media
            student.reference_name = form.reference_name.data if form.reference_name.data else student.reference_name
            student.reference_email = form.reference_email.data if form.reference_email.data else student.reference_email
            student.reference_phone = form.reference_phone.data if form.reference_phone.data else student.reference_phone
            student.reference_relationship = form.reference_relationship.data if form.reference_relationship.data else student.reference_relationship

             # Fetch and assign genres
            genre_ids = request.form.getlist('genres')
            if genre_ids:
                student.genres = db.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()

            # Fetch and assign types
            type_ids = request.form.getlist('types')
            if type_ids:
                student.types = db.session.query(Type).filter(Type.id.in_(type_ids)).all()


        elif user.type == 'Parent':
            parent = Parent.query.filter_by(user_id=user.id).first()

            parent.bio = form.bio.data if form.bio.data else parent.bio
            parent.name = form.name.data if form.name.data else parent.name

        db.session.commit()
        return jsonify(user.to_dict()), 200
    else:
        return jsonify({'errors': form.errors}), 400

# This route is for getting the current user's profile data

@profile_routes.route('/', methods=['GET'])
@login_required
def get_current_user_profile():
    user = current_user
    user_data = {"id": user.id, "username": user.username, "email": user.email, "type": user.type}

    if user.type == 'Student':
        student = Student.query.filter_by(user_id=user.id).first()
        if student:
            user_data['student'] = {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "stage_name": student.stage_name,
                "bio": student.bio,
                "profile_pic": student.profile_pic,
                "phone": student.phone,
                "address_1": student.address_1,
                "address_2": student.address_2,
                "city": student.city,
                "state": student.state,
                "postal_code": student.postal_code,
                "portfolio_url": student.portfolio_url,
                "previous_projects": student.previous_projects,
                "instagram": student.instagram,
                "twitter": student.twitter,
                "facebook": student.facebook,
                "youtube": student.youtube,
                "other_social_media": student.other_social_media,
                "reference_name": student.reference_name,
                "reference_email": student.reference_email,
                "reference_phone": student.reference_phone,
                "reference_relationship": student.reference_relationship,
                "created_date": student.created_date.isoformat(),
                "updated_date": student.updated_date.isoformat(),
            }
            user_data['student']['genres'] = [{'id': genre.id, 'name': genre.name} for genre in student.genres]
            user_data['student']['types'] = [{'id': type_.id, 'name': type_.name} for type_ in student.types]
    elif user.type == 'Parent':
        parent = Parent.query.filter_by(user_id=user.id).first()
        if parent:
            user_data['parent'] = {
                "name": parent.name,
                "bio": parent.bio,
                "logo": parent.logo,
                "created_date": parent.created_date.isoformat(),
                "updated_date": parent.updated_date.isoformat(),
            }

    return jsonify(user_data), 200


@profile_routes.route('/update_genres_types', methods=['PUT'])
@login_required
def update_genres_types():
    user = current_user
    data = request.json

    # Fetch and validate genres and types from the request
    genre_ids = data.get('genres', [])
    type_ids = data.get('types', [])

    if user.type == 'Student':
        student = Student.query.filter_by(user_id=user.id).first()
        if not student:
            return jsonify({"errors": "Student profile not found"}), 404

        # Update genres
        if genre_ids:
            existing_genres = db.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()
            if len(existing_genres) != len(genre_ids):
                return jsonify({"errors": "One or more genres not found"}), 400
            student.genres = existing_genres

        # Update types
        if type_ids:
            existing_types = db.session.query(Type).filter(Type.id.in_(type_ids)).all()
            if len(existing_types) != len(type_ids):
                return jsonify({"errors": "One or more types not found"}), 400
            student.types = existing_types

        db.session.commit()
        return jsonify(student.to_dict()), 200

    return jsonify({"errors": "This route is only available for students"}), 403
