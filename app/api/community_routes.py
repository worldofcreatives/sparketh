# routes/community_routes.py
from flask import Blueprint, request, jsonify
from app.models import db, CommunityPost, PollOption, CommunityComment, User, CommunityPostLike, UserFollow
from flask_login import current_user, login_required
from .helper_functions import contains_inappropriate_content
from sqlalchemy.sql import func
from datetime import datetime, timedelta

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

# Edit a community post
@community_routes.route('/posts/<int:post_id>', methods=['PUT'])
@login_required
def edit_community_post(post_id):
    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    if post.user_id != current_user.id:
        return jsonify({'errors': 'You do not have permission to edit this post'}), 403

    data = request.get_json()
    post_type = data.get('post_type', post.post_type)
    text = data.get('text', post.text)
    image_url = data.get('image_url', post.image_url)
    poll_options = data.get('poll_options', [])

    # Check for inappropriate content
    if contains_inappropriate_content(text):
        return jsonify({'errors': 'Inappropriate content detected'}), 400

    if post_type == 'poll':
        for option_text in poll_options:
            if contains_inappropriate_content(option_text):
                return jsonify({'errors': 'Inappropriate content detected in poll options'}), 400

    post.post_type = post_type
    post.text = text
    post.image_url = image_url
    post.updated_date = datetime.utcnow()

    db.session.commit()

    return jsonify(post.to_dict()), 200

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

# Get all community posts with pagination, filtering, and sorting
@community_routes.route('/posts', methods=['GET'])
@login_required
def get_community_posts():
    """
    sort_by: The field to sort by
        • created_date: Sort by the date the post was created.
        • updated_date: Sort by the date the post was last updated.
        • likes: Sort by the number of likes the post has received.
        • comments: Sort by the number of comments the post has received.

    sort_order: The sorting order
        • asc: Ascending order.
        • desc: Descending order.

    filter_type: Filter posts by type
        • share_art: Filter posts that are of type “share art”.
        • question: Filter posts that are of type “question”.
        • poll: Filter posts that are of type “poll”.

    filter_user: Filter posts by user ID
        • user_id: Filter posts created by a specific user. Replace user_id with the actual ID of the user you want to filter by.

    time_frame: Time frame for sorting likes/comments
        • all_time: Consider all likes/comments regardless of the time they were made.
        • last_30_days: Only consider likes/comments made in the last 30 days.
        • last_week: Only consider likes/comments made in the last week.
        • last_24_hours: Only consider likes/comments made in the last 24 hours.
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    sort_by = request.args.get('sort_by', 'created_date')  # Default sorting by created_date
    sort_order = request.args.get('sort_order', 'desc')  # Default sorting order is descending
    filter_type = request.args.get('filter_type', None)  # Filter by post type
    filter_user = request.args.get('filter_user', None)  # Filter by user ID
    time_frame = request.args.get('time_frame', 'all_time')  # Time frame for sorting likes/comments

    # Base query
    posts_query = CommunityPost.query

    # Apply filters
    if filter_type:
        posts_query = posts_query.filter_by(post_type=filter_type)
    if filter_user:
        posts_query = posts_query.filter_by(user_id=filter_user)

    # Define the time frame for sorting
    now = datetime.utcnow()
    if time_frame == 'last_24_hours':
        start_time = now - timedelta(hours=24)
    elif time_frame == 'last_week':
        start_time = now - timedelta(weeks=1)
    elif time_frame == 'last_30_days':
        start_time = now - timedelta(days=30)
    else:
        start_time = None

    if start_time:
        posts_query = posts_query.outerjoin(CommunityPostLike).outerjoin(CommunityComment)
        posts_query = posts_query.group_by(CommunityPost.id)

        if sort_by == 'likes':
            posts_query = posts_query.add_columns(
                func.count(CommunityPostLike.id).filter(CommunityPostLike.created_date >= start_time).label('like_count')
            ).order_by(func.count(CommunityPostLike.id).filter(CommunityPostLike.created_date >= start_time).desc() if sort_order == 'desc' else func.count(CommunityPostLike.id).filter(CommunityPostLike.created_date >= start_time).asc())

        elif sort_by == 'comments':
            posts_query = posts_query.add_columns(
                func.count(CommunityComment.id).filter(CommunityComment.created_date >= start_time).label('comment_count')
            ).order_by(func.count(CommunityComment.id).filter(CommunityComment.created_date >= start_time).desc() if sort_order == 'desc' else func.count(CommunityComment.id).filter(CommunityComment.created_date >= start_time).asc())

    else:
        # Apply sorting
        if sort_order == 'asc':
            posts_query = posts_query.order_by(getattr(CommunityPost, sort_by).asc())
        else:
            posts_query = posts_query.order_by(getattr(CommunityPost, sort_by).desc())

    # Pagination
    posts = posts_query.paginate(page, per_page, False)

    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    }), 200

# View a single community post
@community_routes.route('/posts/<int:post_id>', methods=['GET'])
@login_required
def get_community_post(post_id):
    post = CommunityPost.query.get(post_id)
    if not post:
        return jsonify({'errors': 'Post not found'}), 404

    return jsonify(post.to_dict()), 200

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

# Edit a community comment
@community_routes.route('/comments/<int:comment_id>', methods=['PUT'])
@login_required
def edit_community_comment(comment_id):
    comment = CommunityComment.query.get(comment_id)
    if not comment:
        return jsonify({'errors': 'Comment not found'}), 404

    if comment.user_id != current_user.id:
        return jsonify({'errors': 'You do not have permission to edit this comment'}), 403

    data = request.get_json()
    text = data.get('text', comment.text)

    # Check for inappropriate content
    if contains_inappropriate_content(text):
        return jsonify({'errors': 'Inappropriate content detected'}), 400

    comment.text = text
    comment.updated_date = datetime.utcnow()

    db.session.commit()

    return jsonify(comment.to_dict()), 200

# Delete a community comment
@community_routes.route('/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_community_comment(comment_id):
    comment = CommunityComment.query.get(comment_id)
    if not comment:
        return jsonify({'errors': 'Comment not found'}), 404

    if comment.user_id != current_user.id:
        return jsonify({'errors': 'You do not have permission to delete this comment'}), 403

    db.session.delete(comment)
    db.session.commit()

    return jsonify({'message': 'Comment deleted successfully'}), 200

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
