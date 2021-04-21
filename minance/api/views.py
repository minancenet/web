import json
import pickle
from datetime import datetime
from functools import wraps

from flask import (
  Blueprint,
  render_template,
  abort,
  Response,
  request
)

from minance import create_app
from minance.models import Asset, Candle

api_old = Blueprint("api_old", __name__)
api = api_old

app = create_app()
V = app.config.get("API_VERSION")

def key_required(clearance):
  def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
      if not "key" in request.args:
        return Response(json.dumps({ "success": False, "cause": "Missing API key."}), mimetype="application/json")

      return f(*args, **kwargs)

    return wrapper
  return decorator

def validateClearance(args, clearance=1):
  if not "key" in args:
    response = {
      "success": False,
      "cause": "Missing API key."
    }

    return False, response
  else:
    key = args["key"]
    # Check if key has correct permissions

    return True, {}

@api.route(f"/api/v{V}/asset/<string:asset_name>/ohlc/<int:minutes>.json")
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

@api.route(f"/api/v{V}/asset/<string:asset_name>/price")
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

@api.route(f"/api/v{V}/orders")
@key_required(clearance=1)
def orders():
  """All orders for Minance."""

  response = {}

  return Response(json.dumps(response), mimetype="application/json")

@api.route(f"/api/v{V}/bot/<int:bot_id>/orders")
@key_required(clearance=1)
def botOrders(bot_id):
  response = {}
  
  return Response(json.dumps(response), mimetype="application/json")