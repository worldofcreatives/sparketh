
# from flask import Blueprint, request, jsonify, render_template
# from flask_login import login_required, current_user
# from app.models import db, Opportunity, Submission
# from app.forms.opportunity_form import OpportunityForm
# from app.forms.submission_form import SubmissionForm
# from sqlalchemy.exc import IntegrityError

# submission_routes= Blueprint('submissions', __name__)


# @submission_routes.route('/<int:id>/submit', methods=['POST'])
# @login_required
# def create_submission(id):

#     form = SubmissionForm()
#     form['csrf_token'].data = request.cookies['csrf_token']
#     opportunity = Opportunity.query.get(id)

#     if form.validate_on_submit():

#         new_submission = Submission(
#             student_id=current_user.id,
#             opportunity_id=opportunity.id,
#             name=form.name.data,
#             notes=form.notes.data,
#             bpm=form.bpm.data,
#             collaborators=form.collaborators.data,
#         )
#         db.session.add(new_submission)
#         db.session.commit()

#         return jsonify(new_submission.to_dict()), 201
#     else:
#         return jsonify({'errors': form.errors}), 400
