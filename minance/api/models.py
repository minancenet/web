from minance import db

class APIKey(db.Model):
  """
  API key model for API access.
  """
  id = db.Column(db.Integer(), primary_key=True)
  # UUID API Key
  clearance = db.Column(db.Integer(), nullable=False, default=1)

  user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))