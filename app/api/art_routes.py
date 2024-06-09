from flask import Blueprint, request, jsonify
from app.models import db, Art
from app.forms import ArtForm

art_routes = Blueprint('art', __name__)

# Upload art
@art_routes.route('/', methods=['POST'])
def upload_art():
    form = ArtForm()
    if form.validate_on_submit():
        new_art = Art(
            name=form.name.data,
            type=form.type.data,
            user_id=form.user_id.data,
            course_id=form.course_id.data,
            media_url=form.media_url.data
        )
        db.session.add(new_art)
        db.session.commit()
        return jsonify(new_art.to_dict()), 201
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
