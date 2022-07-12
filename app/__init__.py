from flask import Flask, render_template, request, redirect, flash, url_for, session, Blueprint
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import urllib.request
import json
import urllib
import os.path
import pprint
from dateutil import relativedelta
from jinja2 import Template
from config import Config
from .routes import global_scope, videos, users, errors
from .models.logger import Logger


# I set the application as Flask object:
app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATE_FOLDER)

# I set the log init and configuration:
logger = Logger()

# Import the configurations from the Config class
app.config.from_object(Config)

# app.config['SESSION_TYPE'] = 'filesystem'

# Here goes the different blueprints used (global scope, users, errors and videos)
app.register_blueprint(users, url_prefix="/admin")
app.register_blueprint(errors, url_prefix="/")
app.register_blueprint(global_scope, url_prefix="/")
app.register_blueprint(videos, url_prefix="/admin")


# Log APP has started:
app.logger.info('App started!')
app.logger.info('Server running on '+Config.SERVER_NAME)