from minance import create_app, register_scheduler
from minance.extensions import socketio

app = create_app()

if __name__ == "__main__":
  register_scheduler(app)

  socketio.init_app(app, logger=True, engineio_logger=True)
  socketio.run(app)