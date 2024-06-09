from .db import db
from .db import environment, SCHEMA, add_prefix_for_prod

# Models
from .user import User
from .student import Student
from .parent import Parent
from .type import Type
from .art import Art
from .course import Course
from .lesson import Lesson
from .teacher import Teacher
from .subject import Subject
