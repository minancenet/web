from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_required, current_user

from minance import create_app, db
from minance.models import Item, Order, Asset
from minance.user.forms import PlaceOrderForm

user = Blueprint("user", __name__)

app = create_app()

@user.route("/account/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
  pOF = PlaceOrderForm()
  if pOF.validate_on_submit():
    if pOF.orderType.data == "buy":
      with app.app_context():
        print(pOF.asset.data.replace(" ", "_").upper())
        asset = Asset.query.filter_by(name=(pOF.asset.data).replace(" ", "_").upper()).first()
        order = Order(orderer=current_user, method=pOF.orderType.data, fee=pOF.fee.data, minimumTrust=pOF.minimumTrust.data, visibility=pOF.visibility.data)

        item = Item(amount=pOF.amount.data, asset=asset)
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