import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  SECRET_KEY = "gsCiQ3UQ0BIKB9HkSPrHIZ68GoFFUMmbS7u3ylHDO1IK04Zlr219nfiD5Rgd6YI7"
  SQLALCHEMY_DATABASE_URI = "postgres://postgres:password@localhost:5432/arbitragedb"

  with open("trade/API_KEY", "r") as f:
    API_KEY = f.read()

  JOBS = [
    {
      "id": "updateAssets",
      "func": "trade.api.api:updateAssets",
      "trigger": "interval",
      "seconds": 30
    },
    {
      "id": "oneMinOHLC",
      "func": "trade.asset.utils:genOneMinOHLC",
      "trigger": "interval",
      "minutes": 1
    }
  ]