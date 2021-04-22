from minance import ma
from minance.models import Asset, Candle

class AssetSchema(ma.Schema):
  class Meta:
    fields = (
      "name",
      "lastUpdated",
      "sellPrice",
      "sellVolume",
      "sellMovingWeek",
      "sellOrderAmount",
      "buyPrice",
      "buyVolume",
      "buyMovingWeek",
      "buyOrderAmount",
      "margin"
    )

    ordered = True
    model = Asset

class CandleSchema(ma.Schema):
  class Meta:
    fields = (
      "priceType",
      "timeFrame",
      "creationDate",
      "open",
      "high",
      "low",
      "close"
    )
    
    ordered = True
    model = Candle