from minance.models import Asset

def test_new_asset(new_asset):
  """
  Given an Asset model
  WHEN a new Asset is created
  THEN check the asset's fields are defined correctly
  """

  assert new_asset.name == "TEST_ASSET"
  assert new_asset.sellPrice == 10.00
  assert new_asset.sellVolume == 11
  assert new_asset.sellMovingWeek == 12
  assert new_asset.sellOrderAmount == 13
  assert new_asset.buyPrice == 14.00
  assert new_asset.buyVolume == 15
  assert new_asset.buyMovingWeek == 16
  assert new_asset.buyOrderAmount == 17