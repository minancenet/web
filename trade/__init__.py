import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_apscheduler import APScheduler

from trade.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "main.home"
login_manager.login_message_category = "alert"

if not app.config.get("DEBUG") or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
  scheduler = APScheduler()
  scheduler.init_app(app)
  scheduler.start()

from trade.main.routes import main
from trade.asset.routes import asset
from trade.auth.routes import auth
from trade.portfolio.routes import portfolio
from trade.api.routes import api

app.register_blueprint(main)
app.register_blueprint(asset)
app.register_blueprint(auth)
app.register_blueprint(portfolio)
app.register_blueprint(api)

from trade import routes