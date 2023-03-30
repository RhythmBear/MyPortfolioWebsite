from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flaskext.markdown import Markdown
from flask_mde import Mde
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import config
import os

# Create Flask app
app = Flask(__name__)
Bootstrap(app)
mde = Mde(app)
markdown = Markdown(app)

# Configure the flask app instance
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)
db = SQLAlchemy(app)

# Configure extentions for the flask app
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

from app import views