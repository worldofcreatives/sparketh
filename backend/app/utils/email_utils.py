import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from itsdangerous import URLSafeTimedSerializer

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')

def send_email(to_email, subject, content):
    message = Mail(
        from_email='7PACKS <info@7packs.com>',
        to_emails=to_email,
        subject=subject,
        html_content=content)

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))

def send_password_reset_email(user):
    serializer = URLSafeTimedSerializer(SECRET_KEY)
    token = serializer.dumps(user.email, salt='password-reset-salt')
    reset_url = f"{os.getenv('FRONTEND_URL')}/reset-password/{token}"
    subject = "Password Reset Requested"
    content = f"To reset your password, click the following link: {reset_url}"
    send_email(user.email, subject, content)
