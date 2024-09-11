from flask.cli import AppGroup
from .users import seed_users, undo_users
from .parents import seed_parents, undo_parents
from .students import seed_students, undo_students
from .types import seed_types, undo_types
from .artworks import seed_art, undo_art
from .courses import seed_courses, undo_courses
from .lessons import seed_lessons, undo_lessons
from .teachers import seed_teachers, undo_teachers
from .subjects import seed_subjects, undo_subjects


from app.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    if environment == 'production':
        # Before seeding in production, you want to run the seed undo
        # command, which will  truncate all tables prefixed with
        # the schema name (see comment in users.py undo_users function).
        # Make sure to add all your other model's undo functions below
        undo_lessons()
        undo_courses()
        undo_art()
        undo_teachers()
        undo_students()
        undo_parents()
        undo_users()
        undo_subjects()
        undo_types()
    seed_types()
    seed_subjects()
    seed_users()
    seed_parents()
    seed_students()
    seed_teachers()
    seed_art()
    seed_courses()
    seed_lessons()



# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_lessons()
    undo_courses()
    undo_art()
    undo_teachers()
    undo_students()
    undo_parents()
    undo_users()
    undo_subjects()
    undo_types()
    # Add other undo functions here
