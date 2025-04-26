from flask import Flask, Response, render_template, redirect, url_for, flash, request, send_from_directory
from datetime import date, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, SkillForm, ResumeForm, ContactForm, ProjectForm, AboutForm, LoginCodeForm, ServiceForms
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from app import app, db, secure_filename
from app.models import *
from app.tasks import send_email, allowed_file, get_lines_of_code, add_new_user
from PIL import Image
from config import Config
import os

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


@app.route('/', methods=['GET', 'POST'])
def home():
    about = About.query.first()
    all_skills = Skills.query.all()
    all_resume_items = Resume.query.all()
    all_services = Services.query.all()
    all_projects = Project.query.all()
    contact_form = ContactForm()
    filters = ['Web', 'Data', 'Automation', "AI"]


    return render_template("index.html",
                           skills=all_skills,
                           resume=all_resume_items,
                           projects=all_projects,
                           project_filters=filters,
                           form=contact_form,
                           years=datetime.today().year - date(2022, 6, 1).year,
                           about_form=about), 200


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # Check to see if a user has been created and create a user if it has not been created
    user = User.query.all()
    if not user:
        add_new_user(username=os.getenv('MY_USERNAME'), password=os.getenv('MY_PASSWORD'))
    else:
        pass

    if request.method == "POST" and login_form.validate_on_submit():
        print(login_form.data)

        user_exists = User.query.filter_by(username=login_form.username.data).first()
        print(user_exists)
        if user_exists:
            print(user_exists.verify_password(login_form.password.data))
            if user_exists.verify_password(login_form.password.data):
                login_user(user_exists)

                flash(message="Login Successful", category="login success")
                return redirect(url_for('edit'))
            else:
                flash(message="Incorrect Password, Try again!", category="wrong password")

        else:
            flash(message="User does not exist! Check details and Try again", category='wrong username')

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
            return redirect('/#about')
        else:
            # If the skill does not exist, add it to the database

            # Add the new skill to the database.
            new_skill = Skills(skill=new_skill_form.skill.data,
                               level=int(new_skill_form.level.data))
            db.session.add(new_skill)
            db.session.commit()

            flash(message=f"Successfully Added {new_skill_form.skill.data}", category="skill_success")
            return redirect('/#about')

    # -------------------------------------- Resume Form ----------------------------------------------------------
    resume = ResumeForm()

    # Check if the Resume Form has been filled has been submitted and Collect the
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

    # ---------------------------------------- PORTFOLIO / PROJECTS ----------------------------------------------
    # Section for adding a new project to the website
    projects = ProjectForm()

    if request.method == "POST" and projects.validate_on_submit():
        print(projects.data.values())
        # pic = request.files['image']
        # new_filename = projects.title.data.replace(' ', '_') + '.' + pic.filename.split('.')[-1]
        new_project = Project(title=projects.title.data,
                              category=projects.category.data,
                              client=projects.client.data,
                              start_date=projects.start_date.data,
                              end_date=projects.end_date.data,
                              url=projects.url.data,
                              description=projects.description.data,
                              image=projects.image.data)

        # # new_photo = photos.save(projects.images.data)
        # if 'image' not in request.files:
        #     flash('No file part')
        #     print("NO IMAGEEE")
        #     return redirect('/edit')

        # # If the user does not select a file, the browser submits an
        # # empty file without a filename.
        # if pic.filename == '':
        #     flash('No selected file')
        #     print("No image at alllll")
        #     return redirect(request.url)

        # # If Image was Uploaded
        # # Rename the filename to match the name of the project

        # if pic and allowed_file(pic.filename):
        #     print("Found Image")
        #     filename = secure_filename(pic.filename)
        #     pic.save(os.path.join(Config.UPLOAD_FOLDER, filename))
        #     os.rename(f'images/{filename}', f'images/{new_filename}')
        #     filename = new_filename

        db.session.add(new_project)
        db.session.commit()

        # return redirect(url_for('download_file', name=filename))

        return redirect('/edit')
    else:
        photo_url = None


    # ---------------------------------------------------- Service --------------------------------------------
    service_form = ServiceForms()

    if request.method == 'POST' and service_form.validate_on_submit():
        new_service_item = Services(service=service_form.service.data,
                                    description=service_form.description.data)

        db.session.add(new_service_item)
        db.session.commit()

        return redirect('/services')

    return render_template('edit.html',
                           skillform=new_skill_form,
                           resume_form=resume,
                           service_form=service_form,
                           project_form=projects,
                           photo_url=photo_url)


@app.route('/skill/<skill_name>', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_name):
    skill = Skills.query.filter_by(skill=skill_name).first()
    skill_form = SkillForm(skill=skill.skill,
                           level=skill.level)

    if request.method == 'POST' and skill_form.validate_on_submit():
        skill.skill = skill_form.skill.data
        skill.level = skill_form.level.data
        db.session.commit()

        return redirect('/#about')

    return render_template('editskills.html',
                           edit_form=skill_form,
                           item=skill.skill)


@app.route('/services/<service>', methods=['POST', 'GET'])
@login_required
def edit_service(service):
    service_edit = Services.query.filter_by(service=service)
    service_form = ServiceForms(title=service_edit.service,
                                subtitle=service_edit.description)

    if request.method == 'POST' and service_form.validate_on_submit():
        service_edit.service = service_form.title.data
        service_edit.description = service_form.subtitle.data

        db.session.commit()

        return redirect('/#services')

    return render_template('editskills.html',
                           edit_form=service,
                           item=service_edit.service)


@app.route('/edit/about', methods=['GET', 'POST'])
@login_required
def edit_about():
    about = About.query.first()
    print(about)

    if about:
        about_form = AboutForm(title=about.title,
                               description=about.description,
                               birthday=about.birthday,
                               Email=about.Email,
                               freelance=about.freelance,
                               city=about.city,
                               country=about.country,
                               resume_summary=about.resume,
                               resume_title=about.resume_title)
    else:
        about_form = AboutForm()

    print(about_form)

    # except Exception:
    #     print("here")
    #     about_form = AboutForm()

    if request.method == 'POST' and about_form.validate_on_submit():
        about = About.query.first()

        if not about:
            about_data = About(title=about_form.title.data,
                               description=about_form.description.data,
                               birthday=about_form.birthday.data,
                               Email=about_form.email.data,
                               freelance=about_form.freelance.data,
                               city=about_form.city.data,
                               country=about_form.country.data,
                               resume=about_form.resume_summary.data,
                               resume_title=about_form.resume_title.data)

            db.session.add(about_data)
            db.session.commit()

        else:
            print(about)
            about.title = about_form.title.data
            about.description = about_form.description.data
            about.birthday = about_form.birthday.data
            about.email = about_form.email.data
            about.freelance = about_form.freelance.data
            about.city = about_form.city.data
            about.country = about_form.country.data
            about.resume = about_form.resume_summary.data
            about.resume_title = about_form.resume_title.data

            db.session.commit()

        return redirect('/#about')

    return render_template('editskills.html', edit_form=about_form, item="Yourself")


@app.route('/resume/<resume_title>', methods=['GET', 'POST'])
@login_required
def edit_resume(resume_title):
    resume = Resume.query.filter_by(title=resume_title).first()
    resume_form = ResumeForm(category=resume.category,
                             title=resume.title,
                             details=resume.details,
                             start_m=resume.start_month,
                             start=resume.start_year,
                             end_m=resume.end_month,
                             end=resume.end_year,
                             organization=resume.organization)

    # When form is submitted edit the required details
    if request.method == 'POST' and resume_form.validate_on_submit():
        resume.category = resume_form.category.data
        resume.title = resume_form.title.data
        resume.details = resume_form.details.data
        resume.start_month = resume_form.start_m.data
        resume.start_year = resume_form.start.data
        resume.end_m = resume_form.end_m.data
        resume.end_year = resume_form.end.data
        resume.organization = resume_form.organization.data

        # commit changes to database
        db.session.commit()

        return redirect('/#resume')

    return render_template('editskills.html',
                           edit_form=resume_form,
                           item=resume.title)


@app.route('/edit_portfolio/<portfolio>', methods=['POST', 'GET'])
@login_required
def edit_portfolio(portfolio):
    portfolio_edit = Project.query.filter_by(title=portfolio).first()
    portfolio_form = ProjectForm(title=portfolio_edit.title,
                                 category=portfolio_edit.category,
                                 client=portfolio_edit.client,
                                 start_date=portfolio_edit.start_date,
                                 end_date=portfolio_edit.end_date,
                                 url=portfolio_edit.url,
                                 description=portfolio_edit.description,
                                 image=portfolio_edit.image
                                 )

    if request.method == 'POST' and portfolio_form.validate_on_submit():
        portfolio_edit.title = portfolio_form.title.data
        portfolio_edit.category = portfolio_form.category.data
        portfolio_edit.client = portfolio_form.client.data
        portfolio_edit.start_date = portfolio_form.start_date.data
        portfolio_edit.end_date = portfolio_form.end_date.data
        portfolio_edit.url = portfolio_form.url.data
        portfolio_edit.description = portfolio_form.description.data
        portfolio_edit.image = portfolio_form.image.data

        db.session.commit()

        return redirect('/#portfolio')

    return render_template('editskills.html',
                           edit_form=portfolio_form,
                           item=portfolio_edit.title)


@app.route('/delete_skill/<skill>', methods=['GET'])
@login_required
def delete_skill(skill):
    skill_to_delete = Skills.query.filter_by(skill=skill).first()
    db.session.delete(skill_to_delete)
    db.session.commit()

    return redirect('/#about')


@app.route('/delete_project/<project>', methods=['GET'])
@login_required
def delete_project(project):
    project_to_delete = Project.query.filter_by(title=project).first()

    os.remove(f"images/{project_to_delete.image}")

    db.session.delete(project_to_delete)
    db.session.commit()
    # After Deleleting the project it's important to delete the project image



    return redirect('/#portfolio')


@app.route('/delete_resume/<resume_item>', methods=['GET'])
@login_required
def delete_resume(resume_item):
    resume_to_delete = Resume.query.filter_by(title=resume_item).first()
    db.session.delete(resume_to_delete)
    db.session.commit()

    return redirect('/#resume')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash(message="Succesfully logged out", category='logout')

    return redirect(url_for('login'))


@app.route('/submit_form', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    print(name, email, subject, message)
    print(os.environ.get("MY_EMAIL"))

    email_response = send_email(sender_name=name,
                                sender_email=os.environ.get("MY_EMAIL"),
                                sender_password=os.environ.get("EMAIL_PASSWORD"),
                                recipient_email="femiemmanuel1990@gmail.com",
                                visitor_email=email,
                                subject=subject,
                                body=message)
    # Check to see if the email was succesfully sent and return a response
    if email_response:
        return 'OK'
    else:
        return 'Failed'
    # Do something with the form data here (e.g., store it in a database)


@app.route('/projects/<project_name>')
def show_port(project_name):
    project = Project.query.filter_by(title=project_name).first()
    return render_template('port-details.html', project=project)


@app.route('/uploads/<name>')
def download_file(name):
    print(name)
    return send_from_directory(Config.DOWNLOAD_FOLDER,
                               name,
                               ), 200


# ______________________________________ DEFINE ERROR HANDLERS _____________________________________#
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500