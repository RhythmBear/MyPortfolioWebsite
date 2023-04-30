import os

from app import db
from werkzeug.security import generate_password_hash
from app.models import User
import smtplib 
from smtplib import SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import ALLOWED_EXTENSIONS
import requests
from requests.exceptions import ConnectionError, ConnectTimeout


def get_lines_of_code():
    try:
        response = requests.get("https://github-loc-api.onrender.com/Rhythmbear")
    except ConnectionError or ConnectTimeout:
        return False, 0
    else:
        if response.json()['response'] == 200:
            return True, response.json()['data']['Total lines']
        else:
            return False, 0


def add_new_user(username, password):
    new_user = User(username=username.title())
    new_user.hash_password(password)
    db.session.add(new_user)
    db.session.commit()


def send_email(sender_name, sender_email, visitor_email, sender_password, recipient_email, subject, body):
    # create message object instance

    print(f"preparing to send email to {recipient_email}")
    message = MIMEMultipart()
    message['From'] = f"{sender_name} From Your Portfolio"
    message['To'] = recipient_email
    message['Subject'] = f"{subject}"
    
    full_message = f"""
    {body}
    This message was sent from your portfolio by {visitor_email}
    """
    # add body to message
    message.attach(MIMEText(full_message, 'plain'))
    
    # create SMTP session
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()
            
            # login to account
            session.login(sender_email, sender_password)
            
            # send mail
            text = message.as_string()
            session.sendmail(sender_email, recipient_email, text)
            
    except TimeoutError or SMTPAuthenticationError:
        print("failed to send email.")

        return False
    else:
        print(f"Letter successfully delivered to {recipient_email}")
        return True


def send_login_email(code):
    recipient_email = os.getenv('USER_EMAIL')
    sender_email = os.getenv('MY_EMAIL')
    sender_password = os.getenv('EMAIL_PASSWORD')

    print(f"preparing to send email to {recipient_email}")
    message = MIMEMultipart()
    message['From'] = f"Your Portfolio Website"
    message['To'] = os.getenv("USER_EMAIL")
    message['Subject'] = f"Your Login Code"

    full_message = f"""
    Use This Six Digit Code to Login into your website.
    {code}
    """
    # add body to message
    message.attach(MIMEText(full_message, 'plain'))

    # create SMTP session
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()

            # login to account
            session.login(sender_email, sender_password)

            # send mail
            text = message.as_string()
            session.sendmail(sender_email, recipient_email, text)

    except TimeoutError or SMTPAuthenticationError:
        print("failed to send email.")

        return False
    else:
        print(f"Letter successfully delivered to {recipient_email}")
        return True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS