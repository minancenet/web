from minance import create_app, register_scheduler

app = create_app("flask.cfg")
register_scheduler(app)