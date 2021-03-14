from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required

user = Blueprint("user", __name__)

@user.route("/account/dashboard")
@login_required
def dashboard():
  return render_template("user/dashboard.html", title="Dashboard")

@user.route("/account/settings")
@login_required
def settings():
  return render_template("user/settings.html", title="Settings")