from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField, DateField
from wtforms import StringField, SubmitField, IntegerField, SelectField, TextAreaField, PasswordField, FileField
from wtforms.validators import DataRequired, URL, NumberRange, Length
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime as dt
from flask_mde import MdeField

cities = ['Abia', 'Adamawa', 'Akwa Ibom', 'Anambra', 'Bauchi', 'Bayelsa', 'Benue', 'Borno', 'Cross River', 'Delta',
          'Ebonyi', 'Edo', 'Ekiti', 'Enugu', 'Gombe', 'Imo', 'Jigawa', 'Kaduna', 'Kano', 'Katsina', 'Kebbi', 'Kogi',
          'Kwara', 'Lagos', 'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo', 'Plateau', 'Rivers', 'Sokoto',
          'Taraba', 'Yobe', 'Zamfara', 'Federal Capital Territory (FCT)']


# ---------------------------- Creating Forms ----------------------- #
class LoginForm(FlaskForm):
    # Creating the form for the Loggin in
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={'style': 'margin : 10px 0 20px'})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'style': 'margin : 10px 0 20px'})
    submit = SubmitField('Login')


class LoginCodeForm(FlaskForm):
    code = IntegerField('Enter The Six Digit Code sent to your mail', validators=[DataRequired()],
                        render_kw={'style': 'margin : 10px 0 20px'})
    submit = SubmitField('Login',
                         render_kw={'style': 'margin : 10px 0 20px'})


class RegisterForm(FlaskForm):
    # Creating the form for the Logginge in
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Your Username', validators=[DataRequired()],
                           render_kw={'style': 'margin : 10px 0 20px'})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={'style': 'margin : 10px 0 20px'})
    password_2 = PasswordField('Re-enter Password', validators=[DataRequired()],
                             render_kw={'style': 'margin : 10px 0 20px'})

    submit = SubmitField('Login')


class SkillForm(FlaskForm):
    # Creating a form for editing and adding new skills
    skill = StringField('Add a New skill', validators=[DataRequired()],
                        render_kw={'style': 'margin : 10px 0 20px'})
    level = IntegerField('Rate yourself, 0-100', validators=[DataRequired(), NumberRange(min=0, max=100)],
                         render_kw={'style': 'margin : 10px 0 20px'})
    submit = SubmitField("Add Skill")


class ServiceForms(FlaskForm):
    # Creating a form for receiving responses
    title = StringField('Add a New Service',
                        validators=[DataRequired()],
                        render_kw={'style': 'margin : 10px 0 20px'}
                        )
    sub_title = StringField('Description of this Service',
                            validators=[DataRequired()],
                            render_kw={'style': 'margin : 10px 0 20px'})
    submit = SubmitField('Add New Service',
                         render_kw={'style': 'margin : 10px 0 20px'})


class ResumeForm(FlaskForm):
    """This form creates a new Resume Item

    """
    category = SelectField('Select Category of Resume', choices=['', 'Education', 'Work Experience'],
                           validators=[DataRequired()],
                           render_kw={'style': 'margin : 10px 0 20px'})
    title = StringField('Title of Degree or Work Position',
                        validators=[DataRequired()],
                        render_kw={'style': 'margin : 10px 0 20px'})
    details = TextAreaField('Details about Education or Work. Write list with html <li> tags',
                            validators=[DataRequired()],
                            render_kw={'style': 'margin : 10px 0 20px'})
    organization = StringField('Name of School or Organization',
                               validators=[DataRequired()],
                               render_kw={'style': 'margin : 10px 0 20px'})
    start_m = SelectField('Start Month', choices=['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                          validators=[DataRequired()],
                          render_kw={'style': 'margin : 10px 0 20px'})
    start = IntegerField('Start Year',
                         validators=[DataRequired(), NumberRange(min=1990, max=dt.now().year)],
                         render_kw={'style': 'margin : 10px 0 20px'})
    end_m = SelectField('End Month',
                        choices=['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        validators=[],
                        render_kw={'style': 'margin : 10px 0 20px'})
    end = IntegerField('End Year',
                       validators=[NumberRange(min=1990, max=dt.now().year)],
                       render_kw={'style': 'margin : 10px 0 20px'})
    submit = SubmitField('Add Resume')


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])


class ProjectForm(FlaskForm):
    title = StringField('Title', 
                        validators=[DataRequired()],
                        render_kw={'placeholder': "What is the Title of Your Project",
                                   'style': 'margin : 10px 0 20px'})
    category = SelectField('Category',
                           choices=['Web', 'Data', 'Automation', "AI"],
                           validators=[DataRequired()],
                           render_kw={'style': 'margin : 10px 0 20px'}) 
    client = StringField("Client", 
                         render_kw={'placeholder': "Who hired You?",
                                    'style': 'margin : 10px 0 20px'})
    start_date = DateField('Start Date',
                           format='%Y-%m-%d',
                           validators=[DataRequired()],
                           render_kw={'style': 'margin : 10px 0 20px'})
    end_date = DateField('End Date',
                         format='%Y-%m-%d',
                         validators=[DataRequired()],
                         render_kw={'style': 'margin : 10px 0 20px'})
    url = StringField('URL', 
                      validators=[DataRequired(), URL()],
                      render_kw={'placeholder': "Where is the Project Hosted?",
                                   'style': 'margin : 10px 0 20px'})

    description = MdeField(validators=[
            DataRequired("Input required"),
            Length(min=15, max=30000)])
    
    # Update URL Field to recieve Image URL instead of file
    image = StringField('Image', 
                      validators=[DataRequired(), URL()],
                      render_kw={'placeholder': "Link to Image for Project?",
                                   'style': 'margin : 10px 0 20px'})
    
    submit = SubmitField('Add Project', render_kw={'style': 'margin : 10px 0 20px'})


class AboutForm(FlaskForm):
    title = StringField('Your Title', validators=[DataRequired()],
                        render_kw={'placeholder': "Who are you",
                        'style': 'margin : 10px 0 20px'})

    description = TextAreaField('About', validators=[DataRequired()],
                              render_kw={'placeholder': "Talk about your self. Separate Paragraphs with |",
                              'style': 'margin : 10px 0 20px'})

    birthday = DateField('Birthday', validators=[DataRequired()],
                         render_kw={'style': 'margin : 10px 0 20px'})
    email = EmailField('Email', validators=[DataRequired()],
                       render_kw={'placeholder': "Your Email address",
                                  'style': 'margin : 10px 0 20px'}
                       )
    freelance = SelectField('Freelance', choices=['Available', 'Not Available'],
                            render_kw={'style': 'margin : 10px 0 20px'}
                            )
    city = SelectField('City', choices=cities, validators=[DataRequired()],
                       render_kw={'style': 'margin : 10px 0 20px'})
    country = StringField('Country', validators=[DataRequired()],
                          render_kw={'style': 'margin : 10px 0 20px'})
    resume_summary = TextAreaField('A quick summary about yourself', validators=[DataRequired()],
                                   render_kw={'placeholder': "Summarize your experience working in this role.",
                                           'style': 'margin : 10px 0 20px'})
    resume_title = StringField('Your Title', validators=[DataRequired()],
                                   render_kw={'placeholder': "For Example, Backend Engineer",
                                              'style': 'margin : 10px 0 20px'})

    submit = SubmitField('Update Details', render_kw={'style': 'margin : 10px 0 20px'})

