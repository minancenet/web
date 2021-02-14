import requests
import logging
import time
import pickle

from datetime import datetime

from trade import app, db
from trade.models import Asset

API_URI = "https://api.hypixel.net/"
API_KEY = app.config.get("API_KEY")

def formulateCall(method):
  r = requests.get(API_URI + method + "?key=" + API_KEY)
  return r.json()

def createAsset(asset):
  """
  Create asset if asset is not initialized in database.
  """
  
  status = asset["quick_status"]

  newAsset = Asset(
    name = status["productId"],
    sellPrice = status["sellPrice"],
    sellVolume = status["sellVolume"],
    sellMovingWeek = status["sellMovingWeek"],
    sellOrderAmount = status["sellOrders"],
    buyPrice = status["buyPrice"],
    buyVolume = status["buyVolume"],
    buyMovingWeek = status["buyMovingWeek"],
    buyOrderAmount = status["buyOrders"]
  )

  db.session.add(newAsset)

def fifteenSecondUpdate():
  """
  Used for grabbing necessary price information and updates every 15 seconds.
  Information crucial for making one minute candles.
  """
  
  assets = formulateCall("skyblock/bazaar")["products"]

  for asset in assets:
    dbAsset = Asset.query.filter_by(name=assets[asset]["product_id"]).first()

    if dbAsset == None:
      createAsset(assets[asset])
    else:
      status = assets[asset]["quick_status"]

      dbAsset.lastUpdated = datetime.utcnow()
      dbAsset.sellPrice = status["sellPrice"]
      dbAsset.sellVolume = status["sellVolume"]
      dbAsset.buyPrice = status["buyPrice"]
      dbAsset.buyVolume = status["buyVolume"]
      
      dbAsset.updatePrices

  db.session.commit()
  app.logger.info("Primary asset data updated.")

def oneMinuteUpdate():
  """
  Used for updated less time sensitive data then the fifteenSecond() call.
  """

  assets = formulateCall("skyblock/bazaar")["products"]

  for asset in assets:
    dbAsset = Asset.query.filter_by(name=assets[asset]["product_id"]).first()
    status = assets[asset]["quick_status"]

    dbAsset.sellMovingWeek = status["sellMovingWeek"]
    dbAsset.sellOrderAmount = status["sellOrders"]
    dbAsset.buyMovingWeek = status["buyMovingWeek"]
    dbAsset.buyOrderAmount = status["buyOrders"]

    sell = assets[asset]["sell_summary"]
    buy = assets[asset]["buy_summary"]

    buyOrders = []
    sellOrders = []
    for order in buy:
      buyOrders.append([order["amount"], order["pricePerUnit"], order["orders"]])
    for order in sell:
      sellOrders.append([order["amount"], order["pricePerUnit"], order["orders"]])

    dbAsset.buyOrders = pickle.dumps(buyOrders)
    dbAsset.sellOrders = pickle.dumps(sellOrders)

  db.session.commit()
  app.logger.info("Secondary asset data updated.")