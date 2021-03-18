from flask import Blueprint, render_template, redirect, url_for

order = Blueprint("order", __name__)

@order.route("/order/<int:order_id>")
def specific_order(order_id):
  return render_template("order/order.html", title="Order #"+str(order_id))