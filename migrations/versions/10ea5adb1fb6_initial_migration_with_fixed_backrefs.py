"""Initial migration with fixed backrefs

Revision ID: 10ea5adb1fb6
Revises: 
Create Date: 2024-06-12 00:26:31.634552

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '10ea5adb1fb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('username', sa.String(length=40), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('salt', sa.String(length=255), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('stripe_customer_id', sa.String(length=120), nullable=True),
    sa.Column('stripe_subscription_id', sa.String(length=120), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('stripe_customer_id'),
    sa.UniqueConstraint('stripe_subscription_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('parents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('profile_pic', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('address_1', sa.String(length=100), nullable=True),
    sa.Column('address_2', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('zip_code', sa.String(length=20), nullable=True),
    sa.Column('stripe_customer_id', sa.String(length=50), nullable=True),
    sa.Column('stripe_subscription_id', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('teachers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('profile_pic', sa.String(length=255), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=True),
    sa.Column('last_name', sa.String(length=50), nullable=True),
    sa.Column('address_1', sa.String(length=100), nullable=True),
    sa.Column('address_2', sa.String(length=100), nullable=True),
    sa.Column('city', sa.String(length=50), nullable=True),
    sa.Column('state', sa.String(length=50), nullable=True),
    sa.Column('zip_code', sa.String(length=20), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('expertise', sa.Text(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('skill_level', sa.String(length=20), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('instructor_id', sa.Integer(), nullable=True),
    sa.Column('materials', sa.JSON(), nullable=True),
    sa.Column('length', sa.Interval(), nullable=False),
    sa.Column('intro_video', sa.String(length=255), nullable=False),
    sa.Column('tips', sa.Text(), nullable=True),
    sa.Column('terms', sa.Text(), nullable=True),
    sa.Column('files', sa.JSON(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['instructor_id'], ['teachers.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('profile_pic', sa.String(length=255), nullable=True),
    sa.Column('bio', sa.Text(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('skill_level', sa.String(length=20), nullable=True),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['parents.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('artworks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('type', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('media_url', sa.String(length=255), nullable=False),
    sa.Column('public', sa.Boolean(), nullable=False),
    sa.Column('open_to_feedback', sa.Boolean(), nullable=False),
    sa.Column('feedback', sa.JSON(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_requests',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('requested_by', sa.Integer(), nullable=False),
    sa.Column('upvotes', sa.Integer(), nullable=False),
    sa.Column('downvotes', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.Column('opted_by', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['opted_by'], ['teachers.id'], ),
    sa.ForeignKeyConstraint(['requested_by'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('course_subjects',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'subject_id')
    )
    op.create_table('course_types',
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('course_id', 'type_id')
    )
    op.create_table('lessons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('created_date', sa.DateTime(), nullable=False),
    sa.Column('updated_date', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('student_course_progress',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('progress', sa.Float(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )
    op.create_table('student_courses',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'course_id')
    )
    op.create_table('student_subjects',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('subject_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['subject_id'], ['subjects.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'subject_id')
    )
    op.create_table('student_types',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.ForeignKeyConstraint(['type_id'], ['types.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'type_id')
    )
    op.create_table('student_lessons',
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('student_id', 'lesson_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_lessons')
    op.drop_table('student_types')
    op.drop_table('student_subjects')
    op.drop_table('student_courses')
    op.drop_table('student_course_progress')
    op.drop_table('lessons')
    op.drop_table('course_types')
    op.drop_table('course_subjects')
    op.drop_table('course_requests')
    op.drop_table('artworks')
    op.drop_table('students')
    op.drop_table('courses')
    op.drop_table('teachers')
    op.drop_table('parents')
    op.drop_table('users')
    op.drop_table('types')
    op.drop_table('subjects')
    # ### end Alembic commands ###
