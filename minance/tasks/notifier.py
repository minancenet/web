import eventlet
eventlet.monkey_patch(thread=True, time=True)

from minance import create_app, db
from minance.models import Asset
from minance.extensions import socketio

app = create_app()

def notifier():
  # Check for item rallies or crashes
  with app.app_context():
    assets = Asset.query.all()
    for asset in assets:
      if asset.changeOverX(120) > 5:
        makeNotification("rally", asset.prettyName, f"{asset.prettyName} has rallied up +{asset.changeOverX(120)}% in the past 30 minutes.")
      if asset.changeOverX(120) < -5:
        makeNotification("crash", asset.prettyName, f"{asset.prettyName} has crashed down {asset.changeOverX(120)}% in the past 30 minutes.")

def makeNotification(type, title, content):
  socketio.emit("notification", {"type": type, "title": title, "content": content}, broadcast=True)
  socketio.sleep(0)