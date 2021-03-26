import pickle

from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_required, current_user

from minance import create_app, db
from minance.models import Item, Order, Asset, User
from minance.user.forms import PlaceOrderForm, UpdateAccountForm

user = Blueprint("user", __name__)

app = create_app()

@user.route("/u/<string:user_username>")
def profile(user_username):
  user = User.query.filter_by(username=user_username).first()
  if not user:
    flash("No user with specified username.", "alert")
    return redirect(url_for("main.home"))
  return render_template("user/profile.html", user=user, title=user.username+"'s Profile")

@user.route("/account/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
  # Portfolio Page

  items = Item.query.filter_by(owner=current_user).all()

  # Transactions Page
  pOF = PlaceOrderForm()
  if pOF.validate_on_submit():
    with app.app_context():
      asset = Asset.query.filter_by(name=(pOF.asset.data).replace(" ", "_").upper()).first()

      if pOF.orderType.data == "buy":
        order = Order(orderer=current_user, method=pOF.orderType.data, fee=pOF.fee.data, minimumTrust=pOF.minimumTrust.data, visibility=pOF.visibility.data)

        item = Item(amount=pOF.amount.data, asset=asset)
        order.items.append(item)
        
        db.session.add(item)
        db.session.add(order)

        db.session.commit()
      else:
        item = Item.query.filter_by(holder=current_user).filter_by(asset=asset).first()
        if not item:
          flash("You do not own that asset in that quantity.", "error")
          return redirect(url_for("user.dashboard"))

        order = Order(orderer=current_user, method=pOF.orderType.data, fee=pOF.fee.data, minimumTrust=pOF.minimumTrust.data, visibility=pOF.visibility.data)

        db.session.add(order)

        db.session.commit()

      return redirect(url_for("user.dashboard")) # TODO Return to specific order page when it is made

  return render_template("user/dashboard.html", items=items, pOF=pOF, title="Dashboard")

@user.route("/account/settings", methods=["GET", "POST"])
@login_required
def settings():
  form = UpdateAccountForm()

  if request.method == "GET":
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.biography.data = current_user.biography
    form.discord.data = current_user.discord

  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.biography = form.biography.data
    current_user.discord = form.discord.data

    db.session.commit()

    return redirect(url_for("main.home")) # Return to public user profile
  
  return render_template("user/settings.html", form=form, title="Settings")