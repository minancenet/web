import requests
import logging
import time
import pickle

from datetime import datetime

from trade import app, db
from trade.models import Asset
from trade.main.notifier import makeNotification

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

def fifteenSecondTasks():
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

def oneMinuteTasks():
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

    historicBuyOrders = pickle.loads(dbAsset.sellHistoricOrders)
    historicSellOrders = pickle.loads(dbAsset.buyHistoricOrders)

    # Adding top current top orders to list of all top orders
    if len(buy) > 0:
      historicBuyOrders.append([datetime.utcnow(), buy[0]["amount"], buy[0]["pricePerUnit"], buy[0]["orders"]])
    if len(sell) > 0:
      historicSellOrders.append([datetime.utcnow(), sell[0]["amount"], sell[0]["pricePerUnit"], sell[0]["orders"]])

    if len(buy) > 0 and buy[0]["pricePerUnit"] != 0:
      dbAsset.margin = ((1 - (sell[0]["pricePerUnit"] / buy[0]["pricePerUnit"]))*100)

    dbAsset.historicBuyOrders = historicBuyOrders
    dbAsset.historicSellOrders = historicSellOrders

  db.session.commit()
  app.logger.info("Secondary asset data updated.")

def fiveMinuteTasks():
  """
  Currently just used for checking stats and pushing notifications.
  """

  # Temporary (Finish later today)
  # assets = Asset.query.all()
  # for asset in assets:
  #   if asset.movingValue >= 0.5:
  #     makeNotification("rally", asset.prettyName, f"{asset.prettyName} has increase 0.5% from the last x hours.")

  # app.logger.info("Notifications sent out to connected clients.")
  pass