import pickle
from datetime import datetime

from minance import create_app, db
from minance.user.models import User, Item

app = create_app()

def updatePortfolioGraphs():
  """Function used for updating the balance portfolio graph on the user dashboard page."""
  with app.app_context():
    users = User.query.all()

    for user in users:
      portfolio = pickle.loads(user.portfolio)
      portfolio.append([datetime.utcnow().timestamp(), user.balance])
      user.portfolio = pickle.dumps(portfolio)

    db.session.commit()