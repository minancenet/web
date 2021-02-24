import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = "gsCiQ3UQ0BIKB9HkSPrHIZ68GoFFUMmbS7u3ylHDO1IK04Zlr219nfiD5Rgd6YI7"
  SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/minancedb"
  DEBUG = True

  # Used for enabling or disabling price and candle updates
  # Used for decreasing required processing power of application
  UPDATE_CANDLES = True

  with open("minance/API_KEY", "r") as f:
    API_KEY = f.read()

  if UPDATE_CANDLES:
    JOBS = [
      {
      "id": "fifteenSecondTasks",
      "func": "minance.api.api:fifteenSecondTasks",
      "trigger": "interval",
      "seconds": 15
      },
      {
        "id": "oneMinuteTasks",
        "func": "minance.api.api:oneMinuteTasks",
        "trigger": "interval",
        "minutes": 1
      },
      {
        "id": "fiveMinuteTasks",
        "func": "minance.api.api:fiveMinuteTasks",
        "trigger": "interval",
        "minutes": 5
      },
      { "id": "oneMinOHLC", "func": "minance.asset.utils:genOneMinOHLC", "trigger": "interval", "minutes": 1 },
      { "id": "threeMinOHLC", "func": "minance.asset.utils:genThreeMinOHLC", "trigger": "interval", "minutes": 3 },
      { "id": "fiveMinOHLC", "func": "minance.asset.utils:genFiveMinOHLC", "trigger": "interval", "minutes": 5 },
      { "id": "fifteenMinOHLC", "func": "minance.asset.utils:genFifteenMinOHLC", "trigger": "interval", "minutes": 15 },
      { "id": "thirtyMinOHLC", "func": "minance.asset.utils:genThirtyMinOHLC", "trigger": "interval", "minutes": 30 },
      { "id": "oneHourOHLC", "func": "minance.asset.utils:genOneHourOHLC", "trigger": "interval", "hours": 1 },
      { "id": "twoHourOHLC", "func": "minance.asset.utils:genTwoHourOHLC", "trigger": "interval", "hours": 2 },
      { "id": "fourHourOHLC", "func": "minance.asset.utils:genFourHourOHLC", "trigger": "interval", "hours": 4 },
      { "id": "sixHourOHLC", "func": "minance.asset.utils:genSixHourOHLC", "trigger": "interval", "hours": 6 },
      { "id": "twelveHourOHLC", "func": "minance.asset.utils:genTwelveHourOHLC", "trigger": "interval", "hours": 12 },
      { "id": "oneDayOHLC", "func": "minance.asset.utils:genOneDayOHLC", "trigger": "interval", "days": 1 },
      { "id": "threeDayOHLC", "func": "minance.asset.utils:genThreeDayOHLC", "trigger": "interval", "days": 3 },
      { "id": "oneWeekOHLC", "func": "minance.asset.utils:genOneWeekOHLC", "trigger": "interval", "days": 7 }
    ]
  else:
    JOBS = [
      {
        "id": "fifteenSecondTasks",
        "func": "minance.api.api:fifteenSecondTasks",
        "trigger": "interval",
        "seconds": 15
      },
      {
        "id": "oneMinuteTasks",
        "func": "minance.api.api:oneMinuteTasks",
        "trigger": "interval",
        "minutes": 1
      }
    ]