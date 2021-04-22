import pytest

from minance import create_app, db
from minance.user.models import User

@pytest.fixture(scope="module")
def test_client():
  _app = create_app("flask_test.cfg")

  with _app.test_client() as test_client:
    with _app.app_context():
      yield test_client

@pytest.fixture(scope="module")
def new_user():
  user = User("user001", "user001@minance.net", "goodPassword")
  
  return user

@pytest.fixture(scope="module")
def init_database(test_client):
  db.create_all()

  yield

  db.drop_all()