from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import config
import os

# Create Flask app
app = Flask(__name__)
Bootstrap(app)


# Configure the flask app instance
CONFIG_TYPE = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
app.config.from_object(CONFIG_TYPE)
db = SQLAlchemy(app)

from app import views