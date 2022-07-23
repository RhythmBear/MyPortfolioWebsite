from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, NumberRange
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from forms import *
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
import os


# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


# Connect to a Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# -------------------------TABLES---------------------------------------- #
# Section for the about section i.e tables and forms


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


# ------------------------------- ROUTES ----------------------------------------------- #
db.create_all()


@app.route('/')
def home():
    all_skills = Skills.query.all()
    all_resume_items = Resume.query.all()
    return render_template("index.html",
                           skills=all_skills,
                           resume=all_resume_items)


# This is commented out becasue it was only needed to create the database
@app.route('/edit', methods=["GET", "POST"])
def edit():
    new_skill_form = SkillForm()

    # Check if the skill form is being called or Submitted
    if request.method == "POST" and new_skill_form.validate_on_submit():
        print('skills')
        print(new_skill_form.skill.data, new_skill_form.level.data)
        # Get new Skill Details and add it to database

        # Check to make sure there is not already an instance of the skill in the database
        skill = Skills.query.filter_by(skill=new_skill_form.skill.data).first()

        if skill:
            # If the skill exists, Change its value to the new value
            skill.level = int(new_skill_form.level.data)
            db.session.commit()

            flash(message=f"Successfully changed {new_skill_form.skill.data} to {new_skill_form.level.data}",
                  category="skill_change_success")
            return redirect('/edit')
        else:
            # If the skill does not exist, add it to the database

            # Add the new skill to the database.
            new_skill = Skills(skill=new_skill_form.skill.data,
                               level=int(new_skill_form.level.data))
            db.session.add(new_skill)
            db.session.commit()

            flash(message=f"Successfully Added {new_skill_form.skill.data}", category="skill_success")
            return redirect('/edit')

    # Resume Form
    resume = ResumeForm()

    # Check if the Resume Form has been filled has is been submitted and Collect the
    # details and add them to the database
    if request.method == "POST" and resume.validate_on_submit():
        print("resume")
        print(resume.data.values())

        new_resume = Resume(title=resume.title.data,
                            details=resume.details.data,
                            organization=resume.organization.data,
                            category=resume.category.data,
                            start_month=resume.start_m.data,
                            start_year=resume.start.data,
                            end_month=resume.end_m.data,
                            end_year=resume.end.data)

        db.session.add(new_resume)
        db.session.commit()
        flash("Successfully Added new Resume Item", category='resume')

        return redirect('/edit')

    return render_template('edit.html',
                           skillform=new_skill_form,
                           resume_form=resume)


@app.route('/portfolio-details')
def show_port():
    return render_template('port-details.html')


if __name__ == "__main__":
    app.run(debug=True)
