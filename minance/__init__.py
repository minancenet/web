import os
import sys
import logging

from flask import Flask

from minance.extensions import (
  db,
  bcrypt,
  login_manager,
  migrate,
  scheduler,
  csrf,
  cor
)

def create_app(config_filename="flask.cfg"):
  """Creating Flask application factories."""
  
  app = Flask(__name__, instance_relative_config=True)
  app.config.from_pyfile(config_filename)
  initialize_extensions(app)
  register_blueprints(app)
  configure_logger(app)

  return app

def initialize_extensions(app):
  """Initializing Flask extensions."""

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  migrate.init_app(app, db)
  csrf.init_app(app)
  cor.init_app(app)

def register_scheduler(app):
  """Registering Flask scheduler tasks"""

  # Stopping flask_apscheduler from running twice
  if not app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    scheduler.init_app(app)
    scheduler.start()

  return None

def register_blueprints(app):
  """Registering Flask blueprints."""

  from minance.main.views import main
  from minance.asset.views import asset
  from minance.auth.views import auth
  from minance.api.views import api
  from minance.user.views import user
  from minance.order.views import order
  from minance.errors.handlers import errors

  app.register_blueprint(main)
  app.register_blueprint(asset)
  app.register_blueprint(auth)
  app.register_blueprint(api)
  app.register_blueprint(user)
  app.register_blueprint(order)
  app.register_blueprint(errors)

def configure_logger(app):
  """Configuring logging."""

  handler = logging.StreamHandler(sys.stdout)
  if not app.logger.handlers:
    app.logger.addHandler(handler)