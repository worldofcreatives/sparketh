# routes/community_routes.py
from flask import Blueprint, request, jsonify
from app.models import db, CommunityPost, PollOption, CommunityComment, User, CommunityPostLike, UserFollow
from flask_login import current_user, login_required
from datetime import datetime
from .helper_functions import contains_inappropriate_content

community_routes = Blueprint('community', __name__)

# ----------------- Community Post Routes -----------------

# Create a new community post
@community_routes.route('/posts', methods=['POST'])
@login_required
def create_community_post():
    if current_user.banned:
        return jsonify({'errors': 'Banned users cannot create posts'}), 403

    data = request.get_json()
    post_type = data.get('post_type')
    text = data.get('text', '')
    image_url = data.get('image_url', None)
    poll_options = data.get('poll_options', [])

    # Check for inappropriate content
    if contains_inappropriate_content(text):
        return jsonify({'errors': 'Inappropriate content detected'}), 400

    if post_type == 'poll':
        for option_text in poll_options:
            if contains_inappropriate_content(option_text):
                return jsonify({'errors': 'Inappropriate content detected in poll options'}), 400

    new_post = CommunityPost(
        user_id=current_user.id,
        post_type=post_type,
        text=text,
        image_url=image_url
    )
    db.session.add(new_post)
    db.session.commit()

    if post_type == 'poll' and poll_options:
        for option_text in poll_options:
            poll_option = PollOption(
                post_id=new_post.id,
                text=option_text
            )
            db.session.add(poll_option)
        db.session.commit()

    return jsonify(new_post.to_dict()), 201

# Delete a community post
@community_routes.route('/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_community_post(post_id):
    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    if post.user_id != current_user.id:
        return jsonify({'errors': 'You do not have permission to delete this post'}), 403

    db.session.delete(post)
    db.session.commit()

    return jsonify({'message': 'Post deleted successfully'}), 200

# Get all community posts with pagination
@community_routes.route('/posts', methods=['GET'])
@login_required
def get_community_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    posts_query = CommunityPost.query.order_by(CommunityPost.created_date.desc())
    posts = posts_query.paginate(page, per_page, False)
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    }), 200

# ----------------- COMMUNITY POST ACTIONS -----------------
# Like a community post
@community_routes.route('/posts/<int:post_id>/like', methods=['POST'])
@login_required
def like_community_post(post_id):
    if current_user.banned:
        return jsonify({'errors': 'Banned users cannot like posts'}), 403

    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    like = CommunityPostLike.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if like:
        return jsonify({'errors': 'Already liked'}), 400

    like = CommunityPostLike(post_id=post_id, user_id=current_user.id)
    db.session.add(like)
    db.session.commit()

    return jsonify(post.to_dict()), 200

# Unlike a community post
@community_routes.route('/posts/<int:post_id>/unlike', methods=['POST'])
@login_required
def unlike_community_post(post_id):
    if current_user.banned:
        return jsonify({'errors': 'Banned users cannot unlike posts'}), 403

    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    like = CommunityPostLike.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    if not like:
        return jsonify({'errors': 'Not liked yet'}), 400

    db.session.delete(like)
    db.session.commit()

    return jsonify(post.to_dict()), 200

# Comment on a community post
@community_routes.route('/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def comment_on_community_post(post_id):
    if current_user.banned:
        return jsonify({'errors': 'Banned users cannot comment on posts'}), 403

    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    data = request.get_json()
    text = data.get('text')
    parent_comment_id = data.get('parent_comment_id', None)

    new_comment = CommunityComment(
        post_id=post.id,
        user_id=current_user.id,
        text=text,
        parent_comment_id=parent_comment_id
    )
    db.session.add(new_comment)
    db.session.commit()

    return jsonify(new_comment.to_dict()), 201

# Follow a user
@community_routes.route('/users/<int:followee_id>/follow', methods=['POST'])
@login_required
def follow_user(followee_id):
    followee = User.query.get(followee_id)
    if not followee:
        return jsonify({'errors': 'User not found'}), 404

    if current_user.id == followee_id:
        return jsonify({'errors': 'You cannot follow yourself'}), 400

    follow = UserFollow(follower_id=current_user.id, followee_id=followee.id)
    db.session.add(follow)
    db.session.commit()
    return jsonify({'message': 'Followed successfully'}), 200

# Unfollow a user
@community_routes.route('/users/<int:followee_id>/unfollow', methods=['POST'])
@login_required
def unfollow_user(followee_id):
    follow = UserFollow.query.filter_by(follower_id=current_user.id, followee_id=followee_id).first()
    if not follow:
        return jsonify({'errors': 'Not following this user'}), 400

    db.session.delete(follow)
    db.session.commit()
    return jsonify({'message': 'Unfollowed successfully'}), 200

# ----------------- MOD ACTIONS -----------------
# Hide/Unhide a post
@community_routes.route('/posts/<int:post_id>/hide', methods=['POST'])
@login_required
def hide_community_post(post_id):
    if current_user.type not in ['teacher', 'parent']:
        return jsonify({'errors': 'Only teachers or parents can hide/unhide posts'}), 403

    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    data = request.get_json()
    hide = data.get('hide', True)
    post.hidden = hide
    db.session.commit()

    return jsonify(post.to_dict()), 200

# Ban/Unban a user
@community_routes.route('/users/<int:user_id>/ban', methods=['POST'])
@login_required
def ban_user(user_id):
    if current_user.type not in ['teacher', 'parent']:
        return jsonify({'errors': 'Only teachers or parents can ban/unban users'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'errors': 'User not found'}), 404

    data = request.get_json()
    ban = data.get('ban', True)
    user.banned = ban
    db.session.commit()

    return jsonify({'message': 'User banned successfully' if ban else 'User unbanned successfully'}), 200

# Report a community post
@community_routes.route('/posts/<int:post_id>/report', methods=['POST'])
@login_required
def report_community_post(post_id):
    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    post.hidden = True
    db.session.commit()

    return jsonify({'message': 'Post reported and hidden for review'}), 200

# Review and unhide a community post
@community_routes.route('/posts/<int:post_id>/review', methods=['POST'])
@login_required
def review_community_post(post_id):
    if current_user.type not in ['teacher', 'parent']:
        return jsonify({'errors': 'Only teachers or parents can review posts'}), 403

    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    data = request.get_json()
    unhide = data.get('unhide', False)

    post.hidden = not unhide
    db.session.commit()

    return jsonify(post.to_dict()), 200
