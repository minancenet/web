from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from minance.models import Item, Order, Asset
from minance.user.forms import PlaceOrderForm

user = Blueprint("user", __name__)

@user.route("/account/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
  pOF = PlaceOrderForm()
  if pOF.validate_on_submit():
    if pOF.orderType == "buy":
      asset = Asset.query.filter_by(name=(pOF.asset.data).replace(" ", "_").capitalize()).first()
      order = Order(orderer=current_user, method=pOF.orderType.data, minimumTrust=pOF.minimumTrust.data)

      item = Item(amount=pOF.amount.data, asset=asset, owner=order.orderer)
      order.items.append(item)
      
      db.session.add(item)
      db.session.add(order)

      db.session.commit()

      return redirect(url_for("user.dashboard"))

  return render_template("user/dashboard.html", pOF=pOF, title="Dashboard")

@user.route("/account/settings")
@login_required
def settings():
  return render_template("user/settings.html", title="Settings")