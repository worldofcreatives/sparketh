from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from datetime import datetime
from app.models import db, Opportunity, Submission, Parent, Student, Genre, Type
from app.forms.opportunity_form import OpportunityForm
from app.forms.submission_form import SubmissionForm
from sqlalchemy.exc import IntegrityError
from ..api.aws_helpers import get_unique_filename, upload_file_to_s3
import os

opportunity_routes = Blueprint('opportunities', __name__)

# GET /api/opportunities - Get all opportunities

@opportunity_routes.route('', methods=['GET'])
@login_required
def get_opportunities():
    opportunities = Opportunity.query.all()
    opportunities_data = [opportunity.to_dict() for opportunity in opportunities]
    return jsonify(opportunities_data), 200

# GET /api/opportunities/:id - Get a single opportunity

@opportunity_routes.route('/<int:id>', methods=['GET'])
@login_required
def get_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if opportunity:
        return jsonify(opportunity.to_dict()), 200
    else:
        return jsonify({"error": "Opportunity not found"}), 404

# POST /api/opportunities - Create a new opportunity

@opportunity_routes.route('', methods=['POST'])
@login_required
def create_opportunity():

    # Ensure the current user is a parent
    if not current_user.is_parent():
        return jsonify({"error": "Unauthorized"}), 403

    # parent = Parent.query.filter_by(user_id=current_user.id).first()

    form = OpportunityForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        new_opportunity = Opportunity(
            name=form.name.data,
            description=form.description.data,
            target_audience=form.target_audience.data,
            budget=form.budget.data,
            guidelines=form.guidelines.data,
            # parent_id=parent.id,
            user_id=current_user.id
        )
        try:
            db.session.add(new_opportunity)
            db.session.commit()
            return jsonify(new_opportunity.to_dict()), 201
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": str(e)}), 500
    elif request.method == 'POST':
        return jsonify(form.errors), 400
    return jsonify({"message": "Submit your opportunity details."}), 200

# PUT /api/opportunities/:id - Update an opportunity

@opportunity_routes.route('/<int:id>', methods=['PUT'])
@login_required
def update_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    # parent = Parent.query.filter_by(user_id=current_user.id).first()
    # if not parent:
    #     return jsonify({"error": "Unauthorized - User is not associated with any parent"}), 403

    if opportunity.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    form = OpportunityForm()
    form["csrf_token"].data = request.cookies["csrf_token"]
    if form.validate_on_submit():
        opportunity.name = form.name.data
        opportunity.description = form.description.data
        opportunity.target_audience = form.target_audience.data
        opportunity.budget = form.budget.data
        opportunity.guidelines = form.guidelines.data

        try:
            db.session.commit()
            return jsonify(opportunity.to_dict()), 200
        except IntegrityError as e:
            db.session.rollback()
            return jsonify({"error": "Database error", "message": str(e)}), 500
    else:
        return jsonify(form.errors), 400


# DELETE /api/opportunities/:id - Delete an opportunity

@opportunity_routes.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_opportunity(id):
    opportunity = Opportunity.query.get(id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    # parent = Parent.query.filter_by(user_id=current_user.id).first()
    # if not parent:
    #     return jsonify({"error": "Unauthorized - User is not associated with any parent"}), 403

    if opportunity.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    try:
        db.session.delete(opportunity)
        db.session.commit()
        return jsonify({"message": "Opportunity deleted successfully"}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "message": str(e)}), 500


# POST /api/opportunities/:id/submit - Create a new submission

def is_allowed_file(filename, allowed_extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions

# Assuming MAX_FILE_SIZE is defined at the top of your file
MAX_FILE_SIZE = 50 * 1024 * 1024  # 5MB in bytes

def file_size_under_limit(file):
    file.seek(0, os.SEEK_END)  # Go to the end of the file
    file_size = file.tell()  # Get the position of EOF
    file.seek(0)  # Reset the file position to the beginning
    return file_size <= MAX_FILE_SIZE

@opportunity_routes.route('/<int:id>/submit', methods=['POST'])
@login_required
def create_submission(id):
    form = SubmissionForm()
    form['csrf_token'].data = request.cookies['csrf_token']
    opportunity = Opportunity.query.get(id)

    if not opportunity:
        return jsonify({'error': 'Opportunity not found.'}), 404

    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year

    # Check the number of submissions the user has made in the current month
    monthly_submission_count = Submission.query.filter(
        Submission.user_id == current_user.id,
        db.extract('month', Submission.created_date) == current_month,
        db.extract('year', Submission.created_date) == current_year
    ).count()

    # Check if the user has already submitted to this opportunity
    existing_submission = Submission.query.filter_by(
        user_id=current_user.id,
        opportunity_id=opportunity.id
    ).first()

    submission_limit_reached = False
    submission_limit_per_opportunity_reached = False

    if current_user.status == 'Accepted':
        if monthly_submission_count >= 3:
            submission_limit_reached = True
        if existing_submission:
            submission_limit_per_opportunity_reached = True
    elif current_user.status in ['Premium Monthly', 'Premium Annual']:
        if monthly_submission_count >= 30:
            submission_limit_reached = True
        if Submission.query.filter_by(user_id=current_user.id, opportunity_id=opportunity.id).count() >= 3:
            submission_limit_per_opportunity_reached = True
    elif current_user.status == 'Major7eague' or current_user.type == 'Parent':
        submission_limit_reached = False
        submission_limit_per_opportunity_reached = False
    else:
        return jsonify({'error': 'You are not allowed to submit.'}), 403

    if submission_limit_reached:
        return jsonify({'error': 'Monthly submission limit reached.'}), 403
    if submission_limit_per_opportunity_reached:
        return jsonify({'error': f'You have reached the submission limit for this opportunity.'}), 403

    if form.validate_on_submit():
        file = form.file.data

        # Check both file type and file size
        if file and is_allowed_file(file.filename, {"mp3", "wav"}) and file_size_under_limit(file):
            file_name = get_unique_filename(file.filename)
            file_url_response = upload_file_to_s3(file, file_name)

            if "url" in file_url_response:
                new_submission = Submission(
                    opportunity_id=opportunity.id,
                    user_id=current_user.id,
                    username=current_user.username,
                    name=form.name.data,
                    notes=form.notes.data,
                    bpm=form.bpm.data,
                    collaborators=form.collaborators.data,
                    file_url=file_url_response["url"],
                )
                db.session.add(new_submission)
                db.session.commit()
                return jsonify(new_submission.to_dict()), 201
            else:
                error_message = file_url_response.get("errors", "Unknown error during file upload.")
                return jsonify({"errors": f"File upload failed: {error_message}"}), 500
        else:
            # Return an appropriate error message if the file type is not allowed or file size exceeds the limit
            if not is_allowed_file(file.filename, {"mp3", "wav"}):
                return jsonify({"error": "File type not allowed"}), 400
            if not file_size_under_limit(file):
                return jsonify({"error": "File size exceeds limit"}), 400

    else:
        return jsonify({'errors': form.errors}), 400


@opportunity_routes.route('/<int:opportunity_id>/submissions/count', methods=['GET'])
@login_required
def get_monthly_submission_count(opportunity_id):
    """
    Gets the number of submissions made by the current user in the current month.
    """
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    submission_count = Submission.query.filter(
        Submission.user_id == current_user.id,
        db.extract('month', Submission.created_date) == current_month,
        db.extract('year', Submission.created_date) == current_year
    ).count()

    return jsonify({'submission_count': submission_count})


@opportunity_routes.route('/<int:opportunity_id>/submissions/user', methods=['GET'])
@login_required
def check_user_submission(opportunity_id):
    """
    Check if the current user has already submitted to the specified opportunity.
    """
    existing_submission = Submission.query.filter_by(
        user_id=current_user.id,
        opportunity_id=opportunity_id
    ).first()

    return jsonify({'has_submitted': existing_submission is not None})


# GET /api/opportunities/submissions - Get all of a user's submissions

@opportunity_routes.route('/submissions/user', methods=['GET'])
@login_required
def get_user_submissions():
    """
    Gets all submissions for the current user.
    """
    user_submissions = Submission.query.filter_by(user_id=current_user.id).all()
    return jsonify([submission.to_dict() for submission in user_submissions]), 200


# GET /api/opportunities/:id/submissions - Get all submissions for an opportunity

@opportunity_routes.route('/<int:id>/submissions', methods=['GET'])
@login_required
def get_submissions_for_opportunity(id):
    opportunity = Opportunity.query.get(id)

    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    # # Query for the parent associated with the current user
    # parent = Parent.query.filter_by(user_id=current_user.id).first()
    # if not parent:
    #     return jsonify({"error": "Access denied. User is not associated with any parent."}), 403

    # # Ensure the current user is authorized to view submissions for the opportunity
    # if opportunity.parent_id != parent.id:
    #     return jsonify({"error": "Access denied. User did not create this opportunity."}), 403

    # Ensure the current user is authorized to view submissions for the opportunity
    if opportunity.user_id != current_user.id:
        return jsonify({"error": "Access denied. User did not create this opportunity."}), 403

    submissions = Submission.query.filter_by(opportunity_id=id).all()
    submissions_list = [submission.to_dict() for submission in submissions]

    return jsonify(submissions_list), 200

# GET /api/opportunities/:opp_id/submissions/:sub_id - Get a specific submission

@opportunity_routes.route('/<int:opp_id>/submissions/<int:sub_id>', methods=['GET'])
@login_required
def get_specific_submission(opp_id, sub_id):
    submission = Submission.query.filter_by(id=sub_id, opportunity_id=opp_id).first()
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    opportunity = Opportunity.query.get(opp_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    # student = Student.query.filter_by(user_id=current_user.id).first()
    # if student and submission.student_id == student.id:
    #     return jsonify(submission.to_dict()), 200

    # parent = Parent.query.filter_by(user_id=current_user.id).first()
    # if parent and opportunity.parent_id == parent.id:
    #     return jsonify(submission.to_dict()), 200

    if opportunity.user_id == current_user.id:
        return jsonify(submission.to_dict()), 200

    return jsonify({"error": "Access denied."}), 403


# PUT /api/opportunities/:opp_id/submissions/:sub_id - Update a submission status

@opportunity_routes.route('/<int:opp_id>/submissions/<int:sub_id>', methods=['PUT'])
@login_required
def update_submission_status(opp_id, sub_id):
    submission = Submission.query.get(sub_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    if submission.opportunity_id != opp_id:
        return jsonify({"error": "Submission does not belong to the given opportunity"}), 400

    # parent = Parent.query.filter_by(user_id=current_user.id).first()
    # if not parent:
    #     return jsonify({"error": "Unauthorized to update submission status - User is not associated with any parent"}), 403

    opportunity = Opportunity.query.get(opp_id)
    if not opportunity or current_user.id != opportunity.user_id:
        return jsonify({"error": "Unauthorized to update submission status"}), 403

    data = request.get_json()
    new_status = data.get('status')

    if new_status not in ['Pending', 'Reviewing', 'Accepted', 'Rejected', 'Archived']:
        return jsonify({"error": "Invalid status value"}), 400

    submission.status = new_status
    db.session.commit()

    return jsonify(submission.to_dict()), 200


# DELETE /api/opportunities/:opp_id/submissions/:sub_id - Delete a submission

@opportunity_routes.route('/<int:opp_id>/submissions/<int:sub_id>', methods=['DELETE'])
@login_required
def delete_submission(opp_id, sub_id):
    submission = Submission.query.get(sub_id)
    if not submission:
        return jsonify({"error": "Submission not found"}), 404

    if submission.opportunity_id != opp_id:
        return jsonify({"error": "Submission does not belong to the given opportunity"}), 400

    opportunity = Opportunity.query.get(opp_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    if opportunity.user_id == current_user.id:
        db.session.delete(submission)
        db.session.commit()
        return jsonify({"message": "Submission successfully deleted"}), 200

    return jsonify({"error": "Unauthorized to delete this submission"}), 403


# GET /api/opportunities/myopps - Get opportunities created by the current user

@opportunity_routes.route('/myopps', methods=['GET'])
@login_required
def user_opportunities():
    current_user_id = current_user.id

    # Fetch opportunities created by the user
    created_opportunities = Opportunity.query.filter_by(user_id=current_user_id).all()
    created_opportunities_data = [opportunity.to_dict() for opportunity in created_opportunities]

    return jsonify(created_opportunities_data)

# GET /api/opportunities/:id/genres_types - Get genres and types for an opportunity

@opportunity_routes.route('/<int:opportunity_id>/update_genres_types', methods=['PUT'])
@login_required
def update_opportunity_genres_types(opportunity_id):
    opportunity = Opportunity.query.get(opportunity_id)
    if not opportunity:
        return jsonify({"error": "Opportunity not found"}), 404

    # Ensure the current user is authorized to update this opportunity
    if opportunity.user_id != current_user.id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.json
    genre_ids = data.get('genres', [])
    type_ids = data.get('types', [])

    # Update genres
    if genre_ids:
        existing_genres = db.session.query(Genre).filter(Genre.id.in_(genre_ids)).all()
        if len(existing_genres) != len(genre_ids):
            return jsonify({"error": "One or more genres not found"}), 400
        opportunity.genres = existing_genres

    # Update types
    if type_ids:
        existing_types = db.session.query(Type).filter(Type.id.in_(type_ids)).all()
        if len(existing_types) != len(type_ids):
            return jsonify({"error": "One or more types not found"}), 400
        opportunity.types = existing_types

    db.session.commit()
    return jsonify(opportunity.to_dict()), 200

# GET /api/opportunities/submissions - Get all submissions

@opportunity_routes.route('/submissions', methods=['GET'])
@login_required
def get_all_submissions():
    # Fetch all submissions
    submissions = Submission.query.all()

    # Prepare data for each submission, including related Opportunity, Genres, and Types
    submissions_data = []
    for submission in submissions:
        opportunity = Opportunity.query.get(submission.opportunity_id)
        genres = [genre.name for genre in submission.genres]
        types = [type.name for type in submission.types]

        submissions_data.append({
            "id": submission.id,
            "name": submission.name,
            "opportunity": opportunity.name if opportunity else "N/A",
            "opp_id": submission.opportunity_id,
            "created_date": submission.created_date.strftime("%Y-%m-%d"),
            "genres": genres,
            "types": types
        })

    return jsonify(submissions_data), 200
