import requests
import logging
import time

from datetime import datetime

from trade import app, db
from trade.models import Asset

API_URI = "https://api.hypixel.net/"
API_KEY = app.config.get("API_KEY")

logger = logging.getLogger(__name__)

def formulateCall(method):
  r = requests.get(API_URI + method + "?key=" + API_KEY)
  return r.json()

def updateAssets():
  assets = formulateCall("skyblock/bazaar")["products"]
  
  for asset in assets:
    searchAsset = Asset.query.filter_by(name=assets[asset]["product_id"]).first()

    asset = assets[asset]["quick_status"]

    if searchAsset == None:
      newAsset = Asset(
        name = asset["productId"],
        sellPrice = round(asset["sellPrice"], 4),
        sellVolume = asset["sellVolume"],
        sellMovingWeek = asset["sellMovingWeek"],
        sellOrders = asset["sellOrders"],
        buyPrice = round(asset["buyPrice"], 4),
        buyVolume = asset["buyVolume"],
        buyMovingWeek = asset["buyMovingWeek"],
        buyOrders = asset["buyOrders"]
      )

      db.session.add(newAsset)
    else:
      searchAsset.lastUpdated = datetime.utcnow()
      searchAsset.sellPrice = round(asset["sellPrice"], 4)
      searchAsset.sellVolume = asset["sellVolume"]
      searchAsset.sellMovingWeek = asset["sellMovingWeek"]
      searchAsset.sellOrders = asset["sellOrders"]
      searchAsset.buyPrice = round(asset["buyPrice"], 4)
      searchAsset.buyVolume = asset["buyVolume"]
      searchAsset.buyMovingWeek = asset["buyMovingWeek"]
      searchAsset.buyOrders = asset["buyOrders"]

      searchAsset.updatePrices

    db.session.commit()
  print("[Arbitrage] Assets updated.")