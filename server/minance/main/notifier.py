from minance import socketio

def makeNotification(type, title, content):
  socketio.emit("notification", {"type": type, "title": title, "content": content}, broadcast=True)