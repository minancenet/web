import pickle
from flask import Blueprint, render_template

from trade.models import Asset

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
  assets = Asset.query.order_by(Asset.sellPrice.desc()).limit(24)
  return render_template("main/index.html", assets=assets, active_page="index", pickle=pickle, enumerate=enumerate, round=round, str=str, title="Home")