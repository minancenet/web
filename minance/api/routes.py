import json
import pickle
from datetime import datetime

from flask import Blueprint, render_template, abort, Response

from minance.models import Asset, Candle

api = Blueprint("api", __name__)

@api.route("/api/v1/asset/<string:asset_name>/ohlc/<int:minutes>.json")
def assetOHLC(asset_name, minutes):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  ohlc = asset.ohlc
  formattedOHLC = []
  for i in ohlc:
    if i.priceType == "sell":
      formattedOHLC.append(i.formattedOHLC)

  ohlc = Candle.query.filter_by(asset=asset).filter_by(timeframe=minutes).all()

  outerOHLC = {
    "sell": [],
    "buy": []
  }
  sellOHLC = []
  buyOHLC = []

  for candle in ohlc:
    if candle.priceType == "buy":
      buyOHLC.append(candle.formattedOHLC)
    else:
      sellOHLC.append(candle.formattedOHLC)

  outerOHLC["sell"] = sellOHLC
  outerOHLC["buy"] = buyOHLC

  return Response(json.dumps(outerOHLC), mimetype="application/json")

@api.route("/api/v1/asset/<string:asset_name>/price")
def assetPrice(asset_name):
  asset = Asset.query.filter_by(name=asset_name).first()
  if not asset:
    abort(404)

  outerPrices = {
    "sell": [],
    "buy": []
  }

  sellPrices = []
  buyPrices = []

  for price in pickle.loads(asset.sellPrices):
    sellPrices.append([price[0].timestamp(), price[1]])
  for price in pickle.loads(asset.buyPrices):
    buyPrices.append([price[0].timestamp(), price[1]])

  outerPrices["sell"] = sellPrices
  outerPrices["buy"] = buyPrices

  return Response(json.dumps(outerPrices), mimetype="application/json")