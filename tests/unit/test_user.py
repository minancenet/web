import pytest

def test_new_user(new_user):
  """
  Given a User model
  WHEN a new User is created
  THEN check the username, email and hashed_password are defined correctly
  """

  assert new_user.username == "user001"
  assert new_user.email == "user001@minance.net"
  assert new_user.checkPassword("goodPassword") == True