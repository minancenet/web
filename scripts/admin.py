# Path hack
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from minance import create_app, db
from minance.models import User, Asset, Item

app = create_app()

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

    print(f"{amount} {asset} added to {user}.")

if __name__ == "__main__":
  if len(sys.argv) > 1:
    if sys.argv[1] == "-g" or sys.argv[1] == "--giveAsset":
      username = input("Username: ")
      asset = input("Asset Name: ")
      amount = input("Amount: ")

      giveAsset(username, asset, int(amount))