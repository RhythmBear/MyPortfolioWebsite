from app import db
from werkzeug.security import generate_password_hash
from app.models import User
import smtplib 
from smtplib import SMTPAuthenticationError
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app import ALLOWED_EXTENSIONS


def add_new_user(username, password):
    hashed_password = generate_password_hash(password=password,
                                             method='pbkdf2:sha256',
                                             salt_length=8)

    new_user = User(username=username,
                    password=hashed_password)
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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS