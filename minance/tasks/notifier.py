import eventlet
eventlet.monkey_patch(thread=True, time=True)

from minance import create_app
from minance.extensions import socketio

app = create_app()

def notifier():
  with app.app_context():
    makeNotification("rally", "Stock of Stonks", "Stock of Stonks is rallying.")
    print("Notifications updated.")

def makeNotification(type, title, content):
  socketio.emit("notification", {"type": type, "title": title, "content": content}, broadcast=True)
  socketio.sleep(0)