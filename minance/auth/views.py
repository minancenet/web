from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from minance import db, bcrypt
from minance.models import User

auth = Blueprint("auth", __name__)

@auth.route("/auth/login", methods=["POST"])
def login():
  next_page = request.args.get("next")

  if current_user.is_authenticated:
    return redirect (next_page) if next_page else redirect(url_for("main.home"))
  
  if request.method == "POST":
    user = User.query.filter_by(username=request.form["username"]).first()
    if user and user.checkPassword(request.form["password"]):
      login_user(user)
    else:
      flash("Invalid credentials.", "error")

  return redirect (next_page) if next_page else redirect(url_for("user.portfolio"))

@auth.route("/auth/logout", methods=["GET", "POST"])
def logout():
  logout_user()
  return redirect(url_for("main.home"))

@auth.route("/auth/register", methods=["POST"])
def register():
  next_page = request.args.get("next")
    
  if current_user.is_authenticated:
    return redirect (next_page) if next_page else redirect(url_for("main.home"))

  if request.method == "POST":
    user = User(request.form["username"], request.form["email"], request.form["password"])

    db.session.add(user)
    db.session.commit()

    flash("Account created successfully.", "success")

  return redirect (next_page) if next_page else redirect(url_for("user.portfolio"))