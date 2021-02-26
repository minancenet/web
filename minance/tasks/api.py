import pickle
import logging
from datetime import datetime, timedelta

from minance import db, create_app
from minance.models import Asset, Candle

app = create_app()

def prepXMinOHLC(minutes):
  with app.app_context():
    assets = Asset.query.all()
    completed = 0
    for count, asset in enumerate(assets):
      completed += genXMinOHLC("sell", minutes, asset)
      completed += genXMinOHLC("buy", minutes, asset)

    print(f"[Minance] [{completed}/{(count+1)*2}] {minutes} minute candles updated.")

def genOneMinOHLC():
  prepXMinOHLC(1)

def genThreeMinOHLC():
  prepXMinOHLC(3)

def genFiveMinOHLC():
  prepXMinOHLC(5)

def genFifteenMinOHLC():
  prepXMinOHLC(15)

def genThirtyMinOHLC():
  prepXMinOHLC(30)

def genOneHourOHLC():
  prepXMinOHLC(60)

def genTwoHourOHLC():
  prepXMinOHLC(120)

def genFourHourOHLC():
  prepXMinOHLC(240)

def genSixHourOHLC():
  prepXMinOHLC(360)

def genTwelveHourOHLC():
  prepXMinOHLC(720)

def genOneDayOHLC():
  prepXMinOHLC(1440)

def genThreeDayOHLC():
  prepXMinOHLC(4320)

def genOneWeekOHLC():
  prepXMinOHLC(10080)


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

def genXMinOHLC(priceType, minutes, asset):
  references = [1, 3, 5, 15, 30, 60, 120, 240, 360, 720, 1440, 4320, 10080]

  if minutes == 1:
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
        creationDate=datetime.utcnow(),
        volume=asset.buyVolume if priceType == "buy" else asset.sellVolume,
        asset=asset
      )

      db.session.add(candle)
      db.session.commit()

      return 1
    else:
      return 0
      
  else:
    # Compile x candles of the previous reference
    # references = [1, 3, 5, 15, 30, 60, 120, 240, 360, 720, 1440, 4320, 10080]
    
    for i, j in enumerate(references):
      if j == minutes:
        for k in range(i-1, -1, -1):
          l = minutes / references[k]
          if l.is_integer():
            index = k
            break

    timeframe = references[index]
    candleAmount = int(minutes/references[index])

    allCandles = Candle.query.filter_by(asset=asset).filter_by(priceType=priceType).filter_by(timeframe=timeframe).order_by(Candle.creationDate.desc())

    # Add number of candles to candles list
    candles = []

    for i, j in enumerate(allCandles):
      if i == candleAmount:
        break
      else:
        candles.append(j)

    # Get minimum price from candles
    minimum = candles[0].low
    for i in candles:
      if i.low < minimum:
        minimum = i.low
      
    # Get maximum price from candles
    maximum = candles[0].high
    for i in candles:
      if i.high > maximum:
        maximum = i.high

    candle = Candle(
      priceType=priceType,
      timeframe=minutes,
      open=candles[-1].open,
      high=maximum,
      low=minimum,
      close=candles[0].close,
      creationDate=datetime.utcnow(),
      volume=asset.buyVolume if priceType == "buy" else asset.sellVolume,
      asset=asset
    )

    for i in candles:
      candle.contains.append(i)

    db.session.add(candle)
    db.session.commit()

    return 1