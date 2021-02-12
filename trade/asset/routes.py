import json
import pickle

from flask import Blueprint, render_template, abort, Response

from trade.models import Asset

asset = Blueprint("asset", __name__)

@asset.route("/assets")
def assets():
  assets = Asset.query.all()

  return render_template("asset/assets.html", assets=assets, active_page="assets", title="Assets")

@asset.route("/asset/<string:asset_name>")
def specific_asset(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  return render_template("asset/asset.html", asset=asset, title=asset.name)

@asset.route("/asset/<string:asset_name>/sell/oneMinOHLC.json")
def assetSellOne(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  ohlc = asset.oneMinOHLC
  formattedOHLC = []
  for i in ohlc:
    if i.priceType == "sell":
      formattedOHLC.append(i.formattedOHLC)

  return Response(json.dumps(formattedOHLC), mimetype="application/json")

@asset.route("/asset/<string:asset_name>/buy/oneMinOHLC.json")
def assetBuyOne(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  ohlc = asset.oneMinOHLC
  formattedOHLC = []
  for i in ohlc:
    if i.priceType == "buy":
      formattedOHLC.append(i.formattedOHLC)

  return Response(json.dumps(formattedOHLC), mimetype="application/json")

@asset.route("/asset/<string:asset_name>/fiveMinOHLC.json")
def asset_five(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  return Response(json.dumps(asset.oneMinOHLC), mimetype="application/json")