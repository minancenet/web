import pickle
import logging
from datetime import datetime, timedelta

from trade import app, db
from trade.models import Asset, Candle

def genOneMinOHLC():
  assets = Asset.query.all()
  completed = 0
  for count, asset in enumerate(assets):
    completed += createCandle("sell", 1, asset)
    completed += createCandle("buy", 1, asset)

  print(f"[Minance] [{completed}/{(count+1)*2}] 1 minute candles updated.")

def genFiveMinOHLC():
  assets = Asset.query.all()
  completed = 0
  for count, asset in enumerate(assets):
    completed += createCandle("sell", 5, asset)
    completed += createCandle("buy", 5, asset)

  print(f"[Minance] [{completed}/{(count+1)*2}] 5 minute candles updated.")

def genThirtyMinOHLC():
  assets = Asset.query.all()
  completed = 0
  for count, asset in enumerate(assets):
    completed += createCandle("sell", 30, asset)
    completed += createCandle("buy", 30, asset)

  print(f"[Minance] [{completed}/{(count+1)*2}] 30 minute candles updated.")

def genOneHourOHLC():
  assets = Asset.query.all()
  completed = 0
  for count, asset in enumerate(assets):
    completed += createCandle("sell", 60, asset)
    completed += createCandle("buy", 60, asset)

  print(f"[Minance] [{completed}/{(count+1)*2}] 60 minute candles updated.")

def getHigh(candlePrices):
  """
  Get highest value from nested list for insertion into Candle object
  """
  maximum = candlePrices[0]

  for i in candlePrices:
    if i[1] > maximum[1]:
      maximum = i

  return maximum[1]

def getLow(candlePrices):
  """
  Get lowest value from nested list for insertion into Candle object
  """
  minimum = candlePrices[0]

  for i in candlePrices:
    if i[1] < minimum[1]:
      minimum = i

  return minimum[1] 

def createCandle(priceType, minutes, asset):
  """
  Create candle object for a certain time frame, asset and price type.
  """
  
  """
  candlesPrices[]
  [0] Datetime object of price addition,
  [1] Price at time of datetime object
  """
  candlePrices = []

  # Adding prices to candlePrices list if the price was added within the last x minutes
  for price in pickle.loads(asset.buyPrices) if priceType == "buy" else pickle.loads(asset.sellPrices):
    if (datetime.utcnow() - timedelta(minutes=minutes)) < price[0]:
      candlePrices.append(price)

  if len(candlePrices) >= 2:
    candle = Candle(
      priceType=priceType,
      timeframe=minutes,
      open=candlePrices[0][1],
      high=getHigh(candlePrices),
      low=getLow(candlePrices),
      close=candlePrices[-1][1],
      volume=asset.buyVolume if priceType == "buy" else asset.sellVolume,
      date=datetime.utcnow(),
      asset=asset
    )

    db.session.add(candle)
    db.session.commit()

    return 1
  else:
    return 0

def findProfitMargin(assetName, purchaseTime, sellTime):
  asset = Asset.query.filter_by(name=assetName).first()

  purchasePrice = 0
  sellPrice = 0
  margin = 0

  for i in pickle.loads(asset.buyPrices):
    if i[0] + timedelta(seconds=10) >= purchaseTime and i[0] - timedelta(seconds=10) <= purchaseTime:
      purchasePrice = i[1]
      break

  for i in pickle.loads(asset.sellPrices):
    if i[0] + timedelta(seconds=30) >= sellTime and i[0] - timedelta(seconds=30) <= sellTime:
      sellPrice = i[1]
      break

  try:
    margin = sellPrice / purchasePrice
  except ZeroDivisionError:
    margin = 0

  return margin