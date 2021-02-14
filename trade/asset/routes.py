import pickle
from datetime import datetime

from flask import Blueprint, render_template, abort, Response, session

from trade.models import Asset
from trade.asset.forms import TrackForm
from trade.asset.utils import findProfitMargin

asset = Blueprint("asset", __name__)

@asset.route("/assets")
def assets():
  assets = Asset.query.all()

  return render_template("asset/assets.html", assets=assets, active_page="assets", title="Assets")

@asset.route("/asset/<string:asset_name>", methods=["GET", "POST"])
def specific_asset(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  form = TrackForm()
  if form.check.data and form.validate():
    purchaseDateTime = datetime.combine(form.purchaseDate.data, form.purchaseTime.data)
    sellDateTime = datetime.combine(form.sellDate.data, form.sellTime.data)

    session["margin"] = findProfitMargin(asset_name, purchaseDateTime, sellDateTime)

  if form.reset.data and form.validate():
    session.pop("margin")

  return render_template("asset/asset.html", asset=asset, form=form, title=asset.name, pickle=pickle)