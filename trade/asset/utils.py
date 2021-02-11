import pickle
import logging
from datetime import datetime, timedelta

from trade import db
from trade.models import Asset

logger = logging.getLogger(__name__)

def genOneMinOHLC():
  assets = Asset.query.all()
  for asset in assets:
    oneMinOHLC = pickle.loads(asset.oneMinOHLC)
    oneMinOHLC.append(createCandle(1, asset))
    asset.oneMinOHLC = pickle.dumps(oneMinOHLC)

def genFiveMinOHLC():
  assets = Asset.query.all()
  for asset in assets:
    fiveMinOHLC = pickle.loads(asset.fiveMinOHLC)
    fiveMinOHLC.append(createCandle(5, asset))
    asset.fiveMinOHLC = pickle.dumps(fiveMinOHLC)

def createCandle(minutes, asset):
  """
  [0]: Epoch Time,
  [1]: Price
  """
  prices = pickle.loads(asset.sellPrices)
  now = datetime.now()

  minutePrices = []

  for price in prices:
    if (now - timedelta(minutes=minutes)) < price[0]:
      minutePrices.append(price)

  """
  [0] Open Time,
  [1] Open Price,
  [2] High Price,
  [3] Low Price,
  [4] Close Price,
  [5] Volume
  """
  candle = [minutePrices[0][0].timestamp(), minutePrices[0][1], None, None, minutePrices[-1][1], asset.sellVolume]

  for data in minutePrices:
    if candle[2]:
      if data[1] > candle[2]:
        candle[2] = data[1]
    else:
      candle[2] = data[1]
    if candle[3]:
      if data[1] < candle[3]:
        candle[3] = data[1]
    else:
      candle[3] = data[1]

  minutePrices = []

  return candle