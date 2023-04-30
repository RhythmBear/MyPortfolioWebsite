from app import db
from itsdangerous.url_safe import URLSafeSerializer as Ser
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(), nullable=False)

    def hash_password(self, password):
        self.password = generate_password_hash(password=password,
                                               method='pbkdf2:sha256',
                                               salt_length=8)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def get_reset_token(self):
        s = Ser(os.getenv('SECRET_KEY'))
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Ser(os.getenv('SECRET_KEY'))
        try:
            user_id = s.loads(token)['user_id']

        except:
            return None

        return User.query.get(user_id)


class Skills(db.Model):
    # I am creating a table in my database for the skills on my website
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.String(250), nullable=False, unique=True)
    level = db.Column(db.Integer, nullable=False)


class Services(db.Model):
    """
    Create New Service entry for Database
    """

    # I am creating a table for the services I offer
    id = db.Column(db.Integer, primary_key=True)
    service = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False, unique=False)


class Resume(db.Model):
    """
    Create New Resume entry For Database
    """
    # I am Creating a Table for filling out my resume details
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    details = db.Column(db.String, nullable=False, unique=False)
    start_month = db.Column(db.String, nullable=False, unique=False)
    start_year = db.Column(db.Integer, nullable=False, unique=False)
    end_month = db.Column(db.String, nullable=True, unique=False)
    end_year = db.Column(db.Integer, nullable=True, unique=False)
    organization = db.Column(db.String, nullable=True, unique=True)
    category = db.Column(db.String, nullable=False, unique=False)


class Project(db.Model):
    """
    Projects Table for the Portfolio Section in the Website
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    client = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(255))

    def __repr__(self):
        return '<Project {}>'.format(self.title)


class About(db.Model):
    """ This contains the Information on the about page"""
    title = db.Column(db.String(255), nullable=False, primary_key=True)
    description = db.Column(db.Text, nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    Email = db.Column(db.String(255), nullable=False)
    freelance = db.Column(db.String, nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    resume = db.Column(db.Text, nullable=False)
    resume_title = db.Column(db.Text, nullable=False)