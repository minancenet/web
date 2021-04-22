from flask_restful import Resource, reqparse

from minance.models import Asset
from minance.asset.schemas import AssetSchema

class AssetListResource(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, help="Name of the asset")
    args = parser.parse_args()
    
    assets = Asset.query.all()

    # Filters
    if args["name"]:
      assets = Asset.query.filter(Asset.name == args["name"]).all()
    else:
      assets = Asset.query.all()

    return AssetSchema(many=True).dump(assets)

class AssetResource(Resource):
  def get(self, asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return AssetSchema().dump(asset)