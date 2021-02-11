from sqlalchemy.sql.expression import func

from trade import app
from trade.models import Asset
from trade.auth.forms import RegistrationForm, LoginForm

@app.context_processor
def processor():
  random_assets = Asset.query.order_by(func.random()).limit(16)

  return dict(
    random_assets=random_assets,
    registrationForm=RegistrationForm(),
    loginForm=LoginForm()
  )