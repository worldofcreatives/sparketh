from flask import Blueprint, request, jsonify
from app.models import db, Lesson
from app.forms import LessonForm

lesson_routes = Blueprint('lessons', __name__)

# Add a lesson to a specific course
@lesson_routes.route('/course/<int:course_id>/lessons', methods=['POST'])
def add_lesson(course_id):
    form = LessonForm()
    if form.validate_on_submit():
        new_lesson = Lesson(
            title=form.title.data,
            course_id=course_id,
            url=form.url.data
        )
        db.session.add(new_lesson)
        db.session.commit()
        return jsonify(new_lesson.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Edit a lesson to a specific course
@lesson_routes.route('/course/<int:course_id>/lessons/<int:lesson_id>', methods=['PUT'])
def edit_lesson(course_id, lesson_id):
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson.query.get_or_404(lesson_id)
        lesson.title = form.title.data
        lesson.url = form.url.data
        db.session.commit()
        return jsonify(lesson.to_dict())
    return jsonify({'errors': form.errors}), 400

# Get all lessons of a specific course
@lesson_routes.route('/course/<int:course_id>/lessons', methods=['GET'])
def get_all_lessons(course_id):
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    return jsonify([lesson.to_dict() for lesson in lessons])
