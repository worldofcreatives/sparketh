# from flask import Blueprint, request, jsonify
# from app.models import db, Course, Type, Subject, Lesson
# from app.forms import CourseForm, LessonForm
# from flask_login import current_user, login_required
# import isodate
# from datetime import timedelta

# course_routes = Blueprint('courses', __name__)

# # Utility function to convert ISO 8601 duration to timedelta
# def parse_duration(duration):
#     try:
#         return isodate.parse_duration(duration)
#     except isodate.ISO8601Error:
#         return None

# # Create a course
# @course_routes.route('/', methods=['POST'])
# def create_course():
#     form = CourseForm()
#     print("🔥🔥🔥 FORM DATA:", form.data)
#     form['csrf_token'].data = request.cookies['csrf_token']
#     if form.validate_on_submit():
#         length = parse_duration(form.length.data)
#         if length is None:
#             return jsonify({'errors': 'Invalid duration format for length'}), 400

#         # Parse materials and files directly from request JSON
#         materials = request.json.get('materials', [])
#         files = request.json.get('files', [])

#         new_course = Course(
#             title=form.title.data,
#             description=form.description.data,
#             skill_level=form.skill_level.data,
#             type=form.type.data,
#             instructor_id=form.instructor_id.data,
#             materials=materials,
#             length=length,
#             intro_video=form.intro_video.data,
#             tips=form.tips.data,
#             terms=form.terms.data,
#             files=files
#         )

#         print("🔥🔥🔥 NEW_COURSE:", new_course)

#         # Handle types and subjects relationships
#         if form.types.data:
#             new_course.types = [Type.query.get(type_id) for type_id in form.types.data]
#         if form.subjects.data:
#             new_course.subjects = [Subject.query.get(subject_id) for subject_id in form.subjects.data]

#         db.session.add(new_course)
#         db.session.commit()
#         return jsonify(new_course.to_dict()), 201
#     return jsonify({'errors': form.errors}), 400

from flask import Blueprint, request, jsonify
from app.models import db, Course, Type, Subject, Teacher, Lesson
from app.forms import CourseForm, LessonForm
from flask_login import current_user, login_required
import isodate

course_routes = Blueprint('courses', __name__)

# Utility function to convert ISO 8601 duration to timedelta
def parse_duration(duration):
    try:
        return isodate.parse_duration(duration)
    except isodate.ISO8601Error:
        return None

# Create a course
@course_routes.route('', methods=['POST'])
@login_required
def create_course():
    # Check if the user is authenticated and is a teacher
    if not current_user.is_authenticated:
        return jsonify({'errors': 'User not authenticated'}), 401

    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can create courses'}), 403

    # Find the teacher record associated with the current user
    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    form = CourseForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        length = parse_duration(form.length.data)
        if length is None:
            return jsonify({'errors': 'Invalid duration format for length'}), 400

        # Parse materials and files directly from request JSON
        materials = request.json.get('materials', [])
        files = request.json.get('files', [])

        new_course = Course(
            title=form.title.data,
            description=form.description.data,
            skill_level=form.skill_level.data,
            type=form.type.data,
            instructor_id=teacher.id,  # Use the teacher's ID from the teacher record
            materials=materials,
            length=length,
            intro_video=form.intro_video.data,
            tips=form.tips.data,
            terms=form.terms.data,
            files=files
        )

        # Handle types and subjects relationships
        if form.types.data:
            new_course.types = [Type.query.get(type_id) for type_id in form.types.data]
        if form.subjects.data:
            new_course.subjects = [Subject.query.get(subject_id) for subject_id in form.subjects.data]

        db.session.add(new_course)
        db.session.commit()
        return jsonify(new_course.to_dict()), 201
    return jsonify({'errors': form.errors}), 400

# Edit a course

@course_routes.route('/<int:course_id>', methods=['PUT'])
@login_required
def edit_course(course_id):
    if not current_user.is_authenticated:
        return jsonify({'errors': 'User not authenticated'}), 401

    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can edit courses'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course = Course.query.get_or_404(course_id)
    if course.instructor_id != teacher.id:
        return jsonify({'errors': 'You are not authorized to edit this course'}), 403

    form = CourseForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate():
        length = parse_duration(form.length.data) if form.length.data else None
        if form.length.data and length is None:
            return jsonify({'errors': 'Invalid duration format for length'}), 400

        if form.title.data:
            course.title = form.title.data
        if form.description.data:
            course.description = form.description.data
        if form.skill_level.data:
            course.skill_level = form.skill_level.data
        if form.type.data:
            course.type = form.type.data
        if 'materials' in request.json:
            course.materials = request.json['materials']
        if form.length.data:
            course.length = length
        if form.intro_video.data:
            course.intro_video = form.intro_video.data
        if form.tips.data:
            course.tips = form.tips.data
        if form.terms.data:
            course.terms = form.terms.data
        if 'files' in request.json:
            course.files = request.json['files']

        # Handle types and subjects relationships
        if form.types.data:
            course.types = [Type.query.get(type_id) for type_id in form.types.data]
        if form.subjects.data:
            course.subjects = [Subject.query.get(subject_id) for subject_id in form.subjects.data]

        db.session.commit()
        return jsonify(course.to_dict())
    return jsonify({'errors': form.errors}), 400


# Add a lesson to a specific course
@course_routes.route('/<int:course_id>/lessons', methods=['POST'])
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
@course_routes.route('/<int:course_id>/lessons/<int:lesson_id>', methods=['PUT'])
def edit_lesson(course_id, lesson_id):
    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson.query.get_or_404(lesson_id)
        lesson.title = form.title.data
        lesson.url = form.url.data
        db.session.commit()
        return jsonify(lesson.to_dict())
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


# Get all lessons of a specific course
@course_routes.route('/<int:course_id>/lessons', methods=['GET'])
def get_all_lessons(course_id):
    lessons = Lesson.query.filter_by(course_id=course_id).all()
    return jsonify([lesson.to_dict() for lesson in lessons])
