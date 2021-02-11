from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, current_user

from trade import db, bcrypt
from trade.models import User

auth = Blueprint("auth", __name__)

@auth.route("/auth/login", methods=["POST"])
def login():
  next_page = request.args.get("next")

  if current_user.is_authenticated:
    return redirect (next_page) if next_page else redirect(url_for("main.home"))
  
  if request.method == "POST":
    user = User.query.filter_by(username=request.form["username"]).first()
    if user and bcrypt.check_password_hash(user.password, request.form["password"]):
      login_user(user)
    else:
      flash("Invalid credentials.", "alert")

  return redirect (next_page) if next_page else redirect(url_for("main.home"))

@auth.route("/auth/logout", methods=["POST"])
def logout():
  logout_user()
  return redirect(url_for("auth.login"))

@auth.route("/auth/register", methods=["POST"])
def register():
  next_page = request.args.get("next")
    
  if current_user.is_authenticated:
    return redirect (next_page) if next_page else redirect(url_for("main.home"))

  if request.method == "POST":
    user = User(
      username=request.form["username"],
      email=request.form["email"],
      password=bcrypt.generate_password_hash(request.form["password"])
    )

    db.session.add(user)
    db.session.commit()

  return redirect (next_page) if next_page else redirect(url_for("main.home"))