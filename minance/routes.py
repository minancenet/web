from sqlalchemy.sql.expression import func

from minance import app
from minance.models import Asset
from minance.auth.forms import RegistrationForm, LoginForm
from minance.main.forms import SearchForm

@app.context_processor
def processor():
  random_assets = Asset.query.order_by(func.random()).limit(16)

  return dict(
    random_assets=random_assets,
    registrationForm=RegistrationForm(),
    searchForm=SearchForm(),
    loginForm=LoginForm()
  )