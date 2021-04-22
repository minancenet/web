from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from minance.models import User, Asset
from minance.schemas import UserSchema, AssetSchema

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

class AssetListResource(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, help="Name of the asset")
    args = parser.parse_args()
    
    assets = Asset.query.all()

    if args["name"]:
      assets = Asset.query.filter(Asset.name == args["name"]).all()
    else:
      assets = Asset.query.all()

    # if "buyPrice" in args:
    #   assets = Asset.query.filter(Asset.buyPrice == int(args["buyPrice"])).all()
    #   if not len(assets) > 0:        
    return AssetSchema(many=True).dump(assets)

class AssetResource(Resource):
  def get(self, asset_id):
    asset = Asset.query.get_or_404(asset_id)
    return AssetSchema().dump(asset)

class UserListResource(Resource):
  def get(self):
    users = User.query.all()
    return UserSchema(many=True).dump(users)

class UserResource(Resource):
  def get(self, user_id):
    user = User.query.get_or_404(user_id)
    return UserSchema().dump(user)

api.add_resource(AssetListResource, "/api/v1/assets", endpoint="assets")
api.add_resource(AssetResource, "/api/v1/asset/<int:asset_id>", endpoint="asset_detail")
api.add_resource(UserListResource, "/api/v1/users", endpoint="users")
api.add_resource(UserResource, "/api/v1/user/<int:user_id>", endpoint="user_detail")