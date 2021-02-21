import pytest
import psycopg2

import testing.postgresql

from minance import create_app, db
from minance.models import Asset

@pytest.fixture(scope="module")
def new_asset():
  asset = Asset(
    name = "TEST_ASSET",
    sellPrice = 10.00,
    sellVolume = 11,
    sellMovingWeek = 12,
    sellOrderAmount = 13,
    buyPrice = 14.00,
    buyVolume = 15,
    buyMovingWeek = 16,
    buyOrderAmount = 17
  )

  return asset

@pytest.fixture(scope="module")
def test_client():
  flask_app = create_app("flask_test.cfg")

  with flask_app.test_client() as test_client:
    with flask_app.app_context():
      yield test_client

@pytest.fixture(scope="module")
def init_database(test_client):
  # Launch a new PostgreSQL server
  with testing.postgresql.Postgresql() as postgresql:
    conn = psycopg2.connect(**postgresql.dsn())
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE minancedb")
    db.create_all()

    yield