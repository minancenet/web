from flask import (
  Blueprint,
  render_template,
  redirect,
  url_for,
  flash,
  abort,
  request
)

from minance import create_app, db
from minance.models import Order

market = Blueprint("market", __name__)

@market.route("/marketplace")
def marketplace():
  page = request.args.get("page", 1, type=int)
  orders = Order.query.order_by(Order.order_date.desc()).paginate(page, per_page=15)

  return render_template("market/marketplace.html", orders=orders, active_page="marketplace", title="Marketplace")

@market.route("/marketplace/filter")
def filterOrders():
  page = request.args.get("page", 1, type=int)
  name = request.args.get("name") if request.args.get("name") else ""
  nameText = "%{}%".format(name).replace(" ", "_").upper()

  orders = Order.query.order_by(Order.order_date.desc())

  if request.args.get("name"):
    orders = orders.filter(Order.items[0].asset.name.like(request.args.get("name"))).order_by(Order.order_date.desc())
  if request.args.get("typeFilter"):
    orders = orders.filter(Order.method == request.args.get("typeFilter")).order_by(Order.order_date.desc())
  if request.args.get("rateFilter"):
    orders = orders.filter(Order.fee == request.args.get("rateFilter")).order_by(Order.order_date.desc())

  return render_template("market/marketplace.html", orders=orders.paginate(page, per_page=15), title="Marketplace")