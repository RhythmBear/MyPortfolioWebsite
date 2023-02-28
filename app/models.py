from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True)
    password = db.Column(db.String(25), nullable=False)


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


