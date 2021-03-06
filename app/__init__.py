from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_uploads import IMAGES, UploadSet, configure_uploads

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login First :)'
login_manager.login_message_category = 'danger'

mail = Mail(app)

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

from app import routes, models


