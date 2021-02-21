from minance import app
from minance.main.routes import home

def testHome():
  client = app.test_client()
  url = "/"

  response = client.get(url)
  assert response.status_code == 200