from flask import Blueprint, request, jsonify
from app.models import db, Course, Lesson
from app.forms import CourseForm, LessonForm

course_routes = Blueprint('courses', __name__)

# Create a course
@course_routes.route('/', methods=['POST'])
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        new_course = Course(
            title=form.title.data,
            description=form.description.data,
            subject=form.subject.data,
            skill_level=form.skill_level.data,
            type=form.type.data,
            instructor_id=form.instructor_id.data,
            materials=form.materials.data,
            length=form.length.data,
            intro_video=form.intro_video.data,
            tips=form.tips.data,
            terms=form.terms.data,
            files=form.files.data
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Edit a course
@course_routes.route('/<int:course_id>', methods=['PUT'])
def edit_course(course_id):
    form = CourseForm()
    if form.validate_on_submit():
        course = Course.query.get_or_404(course_id)
        course.title = form.title.data
        course.description = form.description.data
        course.subject = form.subject.data
        course.skill_level = form.skill_level.data
        course.type = form.type.data
        course.instructor_id = form.instructor_id.data
        course.materials = form.materials.data
        course.length = form.length.data
        course.intro_video = form.intro_video.data
        course.tips = form.tips.data
        course.terms = form.terms.data
        course.files = form.files.data
        db.session.commit()
        return jsonify(course.to_dict())
    return jsonify({'errors': form.errors}), 400

# Get all courses
@course_routes.route('/', methods=['GET'])
def get_all_courses():
    courses = Course.query.all()
    return jsonify([course.to_dict() for course in courses])

# Get course details based on course id
@course_routes.route('/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    course = Course.query.get_or_404(course_id)
    return jsonify(course.to_dict())
