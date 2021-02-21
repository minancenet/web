from minance import create_app

def test_index_page(test_client):
  """
  GIVEN a Flask application configured for testing
  WHEN the '/' page is requested (GET)
  THEN check that the request is valid
  """

  response = test_client.get("/")
  assert response.status_code == 200
  # Checking for main index content
  assert b"Top Hypixel Assets" in response.data
  # Checking if Jinja included templates (footer templates)
  assert b"Hypixel Forums" in response.data