import pickle
from datetime import datetime

from minance import db

candles = db.Table("candles",
  db.Column("containee_id", db.Integer, db.ForeignKey("candle.id")),
  db.Column("container_id", db.Integer, db.ForeignKey("candle.id"))
)

class Candle(db.Model):
  """
  Candle model for open, high, low, close (OHLC) candles.
  """
  id = db.Column(db.Integer(), primary_key=True)
  priceType = db.Column(db.String(), nullable=False)
  timeframe = db.Column(db.Integer(), nullable=False) # Type of candle in minutes
  creationDate = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())

  # OHLC
  open = db.Column(db.Float(precision=4), nullable=False)
  high = db.Column(db.Float(precision=4), nullable=False)
  low = db.Column(db.Float(precision=4), nullable=False)
  close = db.Column(db.Float(precision=4), nullable=False)

  volume = db.Column(db.Integer(), nullable=False)

  """Relation to allow a specific candle to point to other candle objects."""
  contains = db.relationship(
    "Candle", secondary=candles,
    primaryjoin=(candles.c.containee_id == id),
    secondaryjoin=(candles.c.container_id == id),
    backref=db.backref("candles", lazy="dynamic"),
    lazy="dynamic"
  )

  asset_id = db.Column(db.Integer(), db.ForeignKey("asset.id"), nullable=False)

  @property
  def formattedOHLC(self):
    return [self.creationDate.timestamp(), self.open, self.high, self.low, self.close, self.volume]

class Asset(db.Model):
  """
  Main asset class used for storing historical asset data.
  """
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(), nullable=False)
  lastUpdated = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
  
  sellPrice = db.Column(db.Float(precision=4), nullable=False)
  sellPrices = db.Column(db.PickleType(), default=pickle.dumps([]))
  sellVolume = db.Column(db.Integer(), nullable=False)
  sellMovingWeek = db.Column(db.Integer(), nullable=False)
  sellOrderAmount = db.Column(db.Integer(), nullable=False)
  sellOrders = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  sellHistoricOrders = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))

  buyPrice = db.Column(db.Float(precision=4), nullable=False)
  buyPrices = db.Column(db.PickleType(), default=pickle.dumps([]))
  buyVolume = db.Column(db.Integer(), nullable=False)
  buyMovingWeek = db.Column(db.Integer(), nullable=False)
  buyOrderAmount = db.Column(db.Integer(), nullable=False)
  buyOrders = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  buyHistoricOrders = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))

  margin = db.Column(db.Float(precision=2), nullable=False, default=0.0)

  ohlc = db.relationship("Candle", backref="asset", lazy=True)

  items = db.relationship("Item", backref="asset", lazy=True)
  
  @property
  def updatePrices(self):
    sellPrices = pickle.loads(self.sellPrices)
    sellPrices.append([datetime.utcnow(), self.sellPrice])
    self.sellPrices = pickle.dumps(sellPrices)

    buyPrices = pickle.loads(self.buyPrices)
    buyPrices.append([datetime.utcnow(), self.buyPrice])
    self.buyPrices = pickle.dumps(buyPrices)

  def prettyVolume(self, type=""):
    val = ""
    if type == "sell":
      vol = self.sellVolume

    elif type == "buy":
      vol = self.buyVolume

    else: #Combined
      vol = self.buyVolume + self.sellVolume

    if vol > 1000000 and vol < 10000000:
      val = str(vol)[0] + "." + str(vol)[1] + "M"
    elif vol > 10000000 and vol < 100000000:
      val = str(vol)[:2] + "M"
    else:
      val = format(int(vol), ",d")

    return val

  @classmethod
  def calcVolume(self):
    return self.sellVolume + self.buyVolume

  @property
  def movingValue(self):
    sellPrices = pickle.loads(self.sellPrices)
    perChange = 0
    if sellPrices:
      if sellPrices[0][1] != 0:
        perChange = round(((sellPrices[-1][1]) / (sellPrices[0][1]) - 1), 2)
    return perChange

  @property
  def prettyName(self):
    return self.name.title().replace("_", " ")

  def changeOverX(self, cycles):
    sell = pickle.loads(self.sellPrices)
    buy = pickle.loads(self.buyPrices)

    perChange = 0

    sellChange = 0
    if 0 <= cycles < len(sell):
      if sell[-cycles][1] != 0:
        sellChange = (sell[-cycles][1] - sell[-1][1]) / sell[-cycles][1]

    buyChange = 0
    if 0 <= cycles < len(buy):
      if buy[-cycles][1] != 0:
        buyChange = (buy[-cycles][1] - buy[-1][1]) / buy[-cycles][1]

    perChange = round((buyChange + sellChange) / 2, 2)

    return perChange