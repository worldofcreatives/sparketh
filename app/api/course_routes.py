from flask import Blueprint, request, jsonify
from app.models import db, Course, Type, Subject, Teacher, Lesson, student_course_progress_table, Student
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
@login_required
def add_lesson(course_id):
    if not current_user.is_authenticated:
        return jsonify({'errors': 'User not authenticated'}), 401

    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can add lessons'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course = Course.query.get_or_404(course_id)
    if course.instructor_id != teacher.id:
        return jsonify({'errors': 'You are not authorized to add lessons to this course'}), 403

    form = LessonForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    form.course_id.data = course_id
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
@login_required
def edit_lesson(course_id, lesson_id):
    if not current_user.is_authenticated:
        return jsonify({'errors': 'User not authenticated'}), 401

    if current_user.type != 'teacher':
        return jsonify({'errors': 'Only teachers can edit lessons'}), 403

    teacher = Teacher.query.filter_by(user_id=current_user.id).first()
    if not teacher:
        return jsonify({'errors': 'Teacher not found'}), 404

    course = Course.query.get_or_404(course_id)
    if course.instructor_id != teacher.id:
        return jsonify({'errors': 'You are not authorized to edit lessons in this course'}), 403

    lesson = Lesson.query.get_or_404(lesson_id)

    # Update only the fields present in the payload
    payload = request.get_json()
    if 'title' in payload:
        lesson.title = payload['title']
    if 'url' in payload:
        lesson.url = payload['url']

    db.session.commit()
    return jsonify(lesson.to_dict()), 200


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

# -------------

# Add a course to a student's joined courses
@course_routes.route('/join/<int:course_id>', methods=['POST'])
@login_required
def join_course(course_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can join courses'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({'errors': 'Student or Course not found'}), 404

    student.joined_courses.append(course)
    db.session.commit()
    return jsonify(student.to_dict()), 200

# Remove a course from a student's joined courses
@course_routes.route('/unjoin/<int:course_id>', methods=['POST'])
@login_required
def unjoin_course(course_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can unjoin courses'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({'errors': 'Student or Course not found'}), 404

    student.joined_courses.remove(course)
    db.session.commit()
    return jsonify(student.to_dict()), 200

# Toggle lesson completion for a student
@course_routes.route('/<int:course_id>/toggle_lesson/<int:lesson_id>', methods=['POST'])
@login_required
def toggle_lesson_completion(course_id, lesson_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can complete lessons'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    lesson = Lesson.query.get(lesson_id)

    if not student or not lesson or lesson.course_id != course_id:
        return jsonify({'errors': 'Student, Lesson, or Course not found'}), 404

    if lesson in student.completed_lessons:
        student.completed_lessons.remove(lesson)
    else:
        student.completed_lessons.append(lesson)

    db.session.commit()
    return jsonify(student.to_dict()), 200

# Get progress of a student in a course
@course_routes.route('/<int:course_id>/progress', methods=['GET'])
@login_required
def get_progress(course_id):
    if current_user.type != 'student':
        return jsonify({'errors': 'Only students can view progress'}), 403

    student = Student.query.filter_by(user_id=current_user.id).first()
    course = Course.query.get(course_id)

    if not student or not course:
        return jsonify({'errors': 'Student or Course not found'}), 404

    total_lessons = len(course.lessons)
    completed_lessons = len([lesson for lesson in student.completed_lessons if lesson.course_id == course_id])
    progress = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0

    student_course_progress = db.session.query(student_course_progress_table).filter_by(student_id=student.id, course_id=course_id).first()
    if student_course_progress:
        db.session.execute(student_course_progress_table.update().where(
            student_course_progress_table.c.student_id == student.id,
            student_course_progress_table.c.course_id == course_id
        ).values(progress=progress, completed=(progress == 100.0)))
    else:
        db.session.execute(student_course_progress_table.insert().values(
            student_id=student.id, course_id=course_id, progress=progress, completed=(progress == 100.0)))

    db.session.commit()

    return jsonify({'progress': progress}), 200
