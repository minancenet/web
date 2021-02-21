import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from minance.config import Config

app = Flask(__name__)
app.config.from_object(Config)

logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG, format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "main.home"
login_manager.login_message_category = "alert"

socketio = SocketIO(app)

migrate = Migrate()
migrate.init_app(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)

# Used to prevent two scheduler instances from being instantiated
if not app.config.get("DEBUG") or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()

from minance.main.routes import main
from minance.asset.routes import asset
from minance.auth.routes import auth
from minance.portfolio.routes import portfolio
from minance.api.routes import api
from minance.errors.handlers import errors

app.register_blueprint(main)
app.register_blueprint(asset)
app.register_blueprint(auth)
app.register_blueprint(portfolio)
app.register_blueprint(api)
app.register_blueprint(errors)

from minance import routes