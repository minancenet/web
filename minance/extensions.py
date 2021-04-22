from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.home"
login_manager.login_message_category = "alert"
socketio = SocketIO()
migrate = Migrate()
scheduler = APScheduler()
csrf = CSRFProtect()
cor = CORS()
ma = Marshmallow()