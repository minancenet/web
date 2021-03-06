from minance.models import Asset

def findProfitMargin(assetName, purchaseTime, sellTime):
  asset = Asset.query.filter_by(name=assetName).first()

  purchasePrice = 0
  sellPrice = 0
  margin = 0

  for i in pickle.loads(asset.buyPrices):
    if i[0] + timedelta(seconds=10) >= purchaseTime and i[0] - timedelta(seconds=10) <= purchaseTime:
      purchasePrice = i[1]
      break

  for i in pickle.loads(asset.sellPrices):
    if i[0] + timedelta(seconds=30) >= sellTime and i[0] - timedelta(seconds=30) <= sellTime:
      sellPrice = i[1]
      break

  try:
    margin = sellPrice / purchasePrice
  except ZeroDivisionError:
    margin = 0

  return margin