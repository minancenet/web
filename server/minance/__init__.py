import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler
from flask_socketio import SocketIO
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "main.home"
login_manager.login_message_category = "alert"
socketio = SocketIO()
migrate = Migrate()
scheduler = APScheduler()

def create_app(config_filename=None):
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_pyfile(config_filename)
  initialize_extensions(app)
  register_blueprints(app)

  return app

def initialize_extensions(app):
  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  socketio.init_app(app)
  migrate.init_app(app, db)
  scheduler.init_app(app)
  scheduler.start()

def register_blueprints(app):
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