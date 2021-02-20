import pickle
from datetime import datetime

from flask import Blueprint, render_template, abort, Response, session, request

from trade.models import Asset
from trade.asset.forms import TrackForm
from trade.asset.utils import findProfitMargin

asset = Blueprint("asset", __name__)

@asset.route("/assets", methods=["GET", "POST"])
def assets():
  page = request.args.get("page", 1, type=int)
  assets = Asset.query.order_by(Asset.name.asc()).paginate(page, per_page=20)

  return render_template("asset/assets.html", assets=assets, active_page="assets", title="Assets", round=round)

@asset.route("/assets/filter")
def filterAssets():
  page = request.args.get("page", 1, type=int)
  search = request.args.get("search") if request.args.get("search") else ""
  searchText = "%{}%".format(search).replace(" ", "_").upper()
  mainFilter = request.args.get("mainFilter") if request.args.get("mainFilter") else ""
  orderBy = request.args.get("orderBy") if request.args.get("orderBy") else ""

  if mainFilter == "sell":
    if orderBy == "asc":
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.sellPrice.asc())
    else:
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.sellPrice.desc())

  elif mainFilter == "buy":
    if orderBy == "asc":
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.buyPrice.asc())
    else:
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.buyPrice.desc())

  elif mainFilter == "volume":
    if orderBy == "asc":
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.calcVolume().asc())
    else:
      assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.calcVolume().desc())

  elif mainFilter == "margin":
    if orderBy == "asc":
      assets = Asset.query.filter(Asset.buyPrice!=0).filter(Asset.name.like(searchText)).order_by(Asset.margin.asc())
    else:
      assets = Asset.query.filter(Asset.buyPrice!=0).filter(Asset.name.like(searchText)).order_by(Asset.margin.desc())

  else:
    assets = Asset.query.filter(Asset.name.like(searchText)).order_by(Asset.name.asc())

  return render_template("asset/assets.html", assets=assets.paginate(page, per_page=20), active_page="assets", title="Assets", round=round)

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

  return render_template("asset/asset.html", asset=asset, form=form, title=asset.prettyName, pickle=pickle)