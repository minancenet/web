import pickle
import logging

from minance import app, socketio
from flask import Blueprint, render_template, request, redirect, url_for

from minance.models import Asset

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
  assets = Asset.query.order_by(Asset.sellPrice.desc()).limit(24)
  return render_template("main/index.html", assets=assets, active_page="index", pickle=pickle, enumerate=enumerate, round=round, str=str, title="Home")

@main.route("/search", methods=["POST"])
def search():
  next_page = request.args.get("next")

  if request.method == "POST":
    query = request.form["query"]
    query = query.replace(" ", "_")
    asset = Asset.query.filter(Asset.name.ilike(query)).first()
    if asset:
      return redirect(url_for("asset.specific_asset", asset_name=asset.name))
    else:
      return redirect (next_page) if next_page else redirect(url_for("main.home"))