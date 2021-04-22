# Path hack
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from minance import create_app, db
from minance.asset.models import Asset
from minance.user.models import User, Item

app = create_app()

"""
Tools for making development faster.
Remove for production environment.
"""

def giveAsset(user, asset, amount):
  with app.app_context():
    user = User.query.filter_by(username=user).first()
    if not user:
      print("No user with supplied username.")
    
    asset = Asset.query.filter_by(name=asset.upper().replace(" ", "_")).first()
    if not asset:
      print("No asset with supplied asset name.")

    item = Item(owner=user, amount=amount, asset=asset)

    db.session.add(item)
    db.session.commit()

    print(f"{amount} {asset.name} added to {user.username}'s assets.")

def addBalance(user, amount):
  with app.app_context():
    user = User.query.filter_by(username=user).first()
    if not user:
      print("No user with supplied username.")

    user.balance += amount

    db.session.commit()

    print(f"{amount} added to {user.username}'s balance.")

def recreateDB():
  app = create_app()
  with app.app_context():
    db.create_all()

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "-g" or sys.argv[1] == "--giveAsset":
      username = input("Username: ")
      asset = input("Asset Name: ")
      amount = input("Amount: ")
      giveAsset(username, asset, int(amount))

    if sys.argv[1] == "-b" or sys.argv[1] == "--addBalance":
      username = input("Username: ")
      amount = input("Amount: ")
      addBalance(username, int(amount))

    if sys.argv[1] == "-r" or sys.argv[1] == "--recreateDB":
      recreateDB()
      print("DB recreated.")
  else:
    print("No args presented.")