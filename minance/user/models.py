import pickle
from datetime import datetime

from flask_login import UserMixin

from minance import db, bcrypt, login_manager
from minance.api.models import APIKey

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  """
  Main website user model.
  """
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(16), unique=True, nullable=False)
  email = db.Column(db.String(64), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

  biography = db.Column(db.String(512))
  discord = db.Column(db.String(64))

  runner = db.Column(db.Boolean(), nullable=False, default=False)
  trust = db.Column(db.Integer(), nullable=False, default=0)

  balance = db.Column(db.Float(precision=2), default=0, nullable=False)

  items = db.relationship("Item", backref="holder", lazy="dynamic", foreign_keys="Item.user_id")
  assets = db.relationship("Item", backref="owner", lazy="dynamic", foreign_keys="Item.owner_id")
  
  orders = db.relationship("Order", backref="orderer", lazy=True)

  portfolio = db.Column(db.PickleType(), default=pickle.dumps([]))

  api_key = db.relationship("APIKey", backref="user", lazy=True, uselist=False)

  def __init__(self, username, email, password):
    self.username = username
    self.email = email
    self.password = bcrypt.generate_password_hash(password).decode("utf-8")

  def setPassword(self, password):
    """Set user password."""
    self.password = bcrypt.generate_password_hash(password).decode("utf-8")

  def checkPassword(self, value):
    """Check password."""
    return bcrypt.check_password_hash(self.password, value)
    
  def __repr__(self):
    return f"<User {self.username}>"

class Item(db.Model):
  """
  Asset wrapper model for tracking global, in-game items.
  """
  id = db.Column(db.Integer(), primary_key=True)
  amount = db.Column(db.Integer())

  faythe_id = db.Column(db.Integer(), db.ForeignKey("faythe.id")) 
  order_id = db.Column(db.Integer(), db.ForeignKey("order.id"))
  user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
  owner_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
  asset_id = db.Column(db.Integer(), db.ForeignKey("asset.id"))

  def amendItem(self, user, action, amount=None, receiver=None):
    if action == "append":
      self.owner = user

    elif action == "delete":
      pass

    elif action == "transfer":
      pass

  def status(self):
    if self.botHolder != None:
      return "secured"
    elif self.holder != None:
      return "moving"
    else:
      return "unknown"

  def totalWorth(self):
    return "{:,}".format(round(self.asset.sellPrice * self.amount), 2)

class Order(db.Model):
  """
  Model containing data on a specific Minance users order.
  """
  id = db.Column(db.Integer(), primary_key=True)
  status = db.Column(db.String(), nullable=False, default="pending")
  method = db.Column(db.String(), nullable=False)
  minimumTrust = db.Column(db.Integer(), nullable=False)
  fee = db.Column(db.Float(), nullable=False)
  visibility = db.Column(db.String(), nullable=False, default="private")
  order_date = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
  fulfilled_date = db.Column(db.DateTime(), default=datetime.utcnow())

  items = db.relationship("Item", backref="order", lazy=True)

  user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))

  def calcPrice(self):
    if self.method == "buy":
      return "{:,}".format(round(self.items[0].asset.sellPrice * self.items[0].amount, 2))
    else:
      return 0

  def calcReturn(self):
    return "{:,}".format(round((self.items[0].asset.sellPrice * self.items[0].amount)*(self.fee/100), 2))

class Faythe(db.Model):
  """
  A bot within Minecraft that holds user assets.
  Needs substantial work, just create barbones initialization so I don't forgot.
  """
  id = db.Column(db.Integer(), primary_key=True)

  items = db.relationship("Item", backref="botHolder", lazy=True)