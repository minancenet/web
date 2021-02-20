import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = "gsCiQ3UQ0BIKB9HkSPrHIZ68GoFFUMmbS7u3ylHDO1IK04Zlr219nfiD5Rgd6YI7"
  SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/minancedb"
  DEBUG = True

  # Used for enabling or disabling price and candle updates
  # Used for decreasing required processing power of application
  UPDATE_CANDLES = False

  with open("trade/API_KEY", "r") as f:
    API_KEY = f.read()

  if UPDATE_CANDLES:
    JOBS = [
      {
      "id": "fifteenSecondTasks",
      "func": "trade.api.api:fifteenSecondTasks",
      "trigger": "interval",
      "seconds": 15
      },
      {
        "id": "oneMinuteTasks",
        "func": "trade.api.api:oneMinuteTasks",
        "trigger": "interval",
        "minutes": 1
      },
      {
        "id": "fiveMinuteTasks",
        "func": "trade.api.api:fiveMinuteTasks",
        "trigger": "interval",
        "minutes": 5
      },
      { "id": "oneMinOHLC", "func": "trade.asset.utils:genOneMinOHLC", "trigger": "interval", "minutes": 1 },
      { "id": "threeMinOHLC", "func": "trade.asset.utils:genThreeMinOHLC", "trigger": "interval", "minutes": 3 },
      { "id": "fiveMinOHLC", "func": "trade.asset.utils:genFiveMinOHLC", "trigger": "interval", "minutes": 5 },
      { "id": "fifteenMinOHLC", "func": "trade.asset.utils:genFifteenMinOHLC", "trigger": "interval", "minutes": 15 },
      { "id": "thirtyMinOHLC", "func": "trade.asset.utils:genThirtyMinOHLC", "trigger": "interval", "minutes": 30 },
      { "id": "oneHourOHLC", "func": "trade.asset.utils:genOneHourOHLC", "trigger": "interval", "hours": 1 },
      { "id": "twoHourOHLC", "func": "trade.asset.utils:genTwoHourOHLC", "trigger": "interval", "hours": 2 },
      { "id": "fourHourOHLC", "func": "trade.asset.utils:genFourHourOHLC", "trigger": "interval", "hours": 4 },
      { "id": "sixHourOHLC", "func": "trade.asset.utils:genSixHourOHLC", "trigger": "interval", "hours": 6 },
      { "id": "twelveHourOHLC", "func": "trade.asset.utils:genTwelveHourOHLC", "trigger": "interval", "hours": 12 },
      { "id": "oneDayOHLC", "func": "trade.asset.utils:genOneDayOHLC", "trigger": "interval", "days": 1 },
      { "id": "threeDayOHLC", "func": "trade.asset.utils:genThreeDayOHLC", "trigger": "interval", "days": 3 },
      { "id": "oneWeekOHLC", "func": "trade.asset.utils:genOneWeekOHLC", "trigger": "interval", "days": 7 }
    ]
  else:
    JOBS = [
      {
        "id": "fifteenSecondTasks",
        "func": "trade.api.api:fifteenSecondTasks",
        "trigger": "interval",
        "seconds": 15
      },
      {
        "id": "oneMinuteTasks",
        "func": "trade.api.api:oneMinuteTasks",
        "trigger": "interval",
        "minutes": 1
      }
    ]