# contact_routes.py
from flask import Blueprint, request, jsonify
from app.utils.email_utils import send_email

contact_routes = Blueprint('contact', __name__)

@contact_routes.route('', methods=['POST'])
def contact():
    data = request.get_json()
    print(data)
    name = data.get('name')
    email = data.get('email')
    subject = data.get('subject')
    message = data.get('message')

    if not all([name, email, subject, message]):
        return jsonify({'error': 'All fields are required.'}), 400

    email_body = f"""
    Name: {name}
    Email: {email}
    Subject: {subject}
    Message: {message}
    """

    print(email_body)

    try:
        send_email('info@sparketh.com', f'Contact Us Form: {subject}', email_body)
        print("Email function called")
        return jsonify({'message': 'Message sent successfully!'}), 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500
