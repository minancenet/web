from flask import (
  Blueprint,
  render_template,
  redirect,
  url_for,
  flash,
  abort
)

from minance import create_app, db
from minance.models import Order

market = Blueprint("market", __name__)

@market.route("/marketplace")
def marketplace():
  orders = Order.query.order_by(Order.order_date.desc())

  return render_template("market/marketplace.html", orders=orders, title="Marketplace")