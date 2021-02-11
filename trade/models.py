import pickle
from datetime import datetime

from flask_login import UserMixin, current_user

from trade import db, login_manager

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(16), unique=True, nullable=False)
  email = db.Column(db.String(64), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

  assets = db.relationship("UserAsset", backref="holder", lazy=True)

class UserAsset(db.Model):
  id = db.Column(db.Integer(), primary_key=True)

  specific_values = db.Column(db.PickleType(), default=pickle.dumps([]))
  # Example - List
  # [
  #   [datetime.utcnow(), amount]
  # ]

  user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)
  asset_id = db.Column(db.Integer(), db.ForeignKey("asset.id"), nullable=False)

  @property
  def amount(self):
    loaded = pickle.loads(self.specific_values)
    totalAmount = 0
    for i in loaded:
      totalAmount += i[1]

    return totalAmount

  @property
  def worth(self):
    totalWorth = round((self.amount * self.asset.sellPrice), 4)

    val = str(totalWorth)
    if totalWorth > 1000000 and totalWorth < 10000000:
      val = str(totalWorth)[0] + "." + str(totalWorth)[1] + "M"
    elif totalWorth > 10000000 and totalWorth < 100000000:
      val = str(totalWorth)[:2] + "M"
    elif totalWorth > 100000000 and totalWorth < 1000000000:
      val = str(totalWorth)[:3] + "M"
    elif totalWorth > 1000000000 and totalWorth < 10000000000:
      val = str(totalWorth)[0] + "." + str(totalWorth)[1] + "B"
    else:
      val = format(int(val), ",d")
      
    return val

class Asset(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(), nullable=False)
  
  sellPrice = db.Column(db.Float(precision=4), nullable=False)
  sellVolume = db.Column(db.Integer(), nullable=False)
  sellMovingWeek = db.Column(db.Integer(), nullable=False)
  sellOrders = db.Column(db.Integer(), nullable=False)

  buyPrice = db.Column(db.Float(precision=4), nullable=False)
  buyVolume = db.Column(db.Integer(), nullable=False)
  buyMovingWeek = db.Column(db.Integer(), nullable=False)
  buyOrders = db.Column(db.Integer(), nullable=False)

  oneMinOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  fiveMinOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  tenMinOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  thirtyMinOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  # oneHourOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  # sixHourOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  # oneDayOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  # oneWeekOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))
  # oneMonthOHLC = db.Column(db.PickleType(), nullable=False, default=pickle.dumps([]))

  userAssets = db.relationship("UserAsset", backref="asset", lazy=True)

  # -------------------------------------------------------------

  @property
  def updatePrices(self):
    sellPrices = pickle.loads(self.sellPrices)
    sellPrices.append([datetime.now(), self.sellPrice])
    self.sellPrices = pickle.dumps(sellPrices)

    buyPrices = pickle.loads(self.buyPrices)
    buyPrices.append(self.buyPrice)
    self.buyPrices = pickle.dumps(buyPrices)

  @property
  def movingValue(self):
    sellPrices = pickle.loads(self.sellPrices)
    perChange = 0
    if sellPrices:
      if sellPrices[-1][1] != 0:
        perChange = round((sellPrices[0][1] / sellPrices[-1][1] - 1), 2)
    return perChange

  @classmethod
  def calcMargin(self):
    margin = 0
    if self.buyPrice != 0:
      margin = 1 - (self.sellPrice / self.buyPrice)

    return margin

  @property
  def printMargin(self):
    margin = 0 
    if self.buyPrice != 0:
      margin = round((1 - (self.sellPrice / self.buyPrice))*100, 2)

    return margin

  @property
  def volumeAbr(self):
    combinedVolume = self.sellVolume + self.buyVolume
    val = str(combinedVolume)
    if combinedVolume > 1000000 and combinedVolume < 10000000:
      val = str(combinedVolume)[0] + "." + str(combinedVolume)[1] + "M"
    elif combinedVolume > 10000000 and combinedVolume < 100000000:
      val = str(combinedVolume)[:2] + "M"
    else:
      val = format(int(val), ",d")

    return val