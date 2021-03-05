from flask import Blueprint, render_template, url_for, redirect

user = Blueprint("user", __name__)

@user.route("/account/dashboard")
def dashboard():
  return render_template("user/dashboard.html", title="Dashboard")