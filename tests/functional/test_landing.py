import pytest

def test_landing(test_client):
  """
  GIVEN a Flask application configured for testing
  WHEN the '/' page is requested (GET)
  THEN check that the response is valid
  """

  response = test_client.get("/")
  
  assert response.status_code == 200
  assert b"Top Hypixel Assets" in response.data # Main page content
  assert b"Minance is a real-time Hypixel Skyblock bazaar tracker." in response.data # Dropdown modal content
  assert b"2021" in response.data # Footer content