from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SkillForm, ServiceForms, ResumeForm
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from app import app, db
from app.models import *



# Create Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def login_manager(user_id):
    return User.query.get(int(user_id))
# -------------------------TABLES---------------------------------------- #


# Section for the about section i.e tables and forms

# Creating a simple table that will be used for the User


# ------------------------------- ROUTES ----------------------------------------------- #
db.create_all()


@app.route('/')
def home():
    all_skills = Skills.query.all()
    all_resume_items = Resume.query.all()
    return render_template("index.html",
                           skills=all_skills,
                           resume=all_resume_items)


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if request.method == "POST" and login_form.validate_on_submit():
        print(login_form.data)

        user_exists = User.query.filter_by(username=login_form.username.data).first()
        print(user_exists)
        if user_exists:
            user_password = user_exists.password
            password_correct = check_password_hash(pwhash=user_password,
                                                   password=login_form.password.data)

            if password_correct:
                login_user(user_exists)

                flash(message="Login Successful", category="login success")
                return redirect(url_for('edit'))
            else:
                flash(message="Invalid Details", category="wrong password")

        else:
            flash(message="Invalid User, Check details and Try again", category='wrong username')

    return render_template('login.html', login_form=login_form)


# This is commented out becasue it was only needed to create the database

@app.route('/edit', methods=["GET", "POST"])
@login_required
def edit():
    new_skill_form = SkillForm()

    if not current_user.is_authenticated:
        return redirect('/login')

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


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="Succesfully logged out", category='logout')

    return redirect(url_for('login'))


@app.route('/portfolio-details')
def show_port():
    return render_template('port-details.html')