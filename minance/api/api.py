from flask import Blueprint
from flask_restful import Api

from minance.asset.resources import AssetListResource, AssetResource
from minance.user.resources import UserListResource, UserResource

api_bp = Blueprint("api", __name__)
api = Api(api_bp)

api.add_resource(AssetListResource, "/api/v1/assets", endpoint="assets")
api.add_resource(AssetResource, "/api/v1/asset/<int:asset_id>", endpoint="asset_detail")
api.add_resource(UserListResource, "/api/v1/users", endpoint="users")
api.add_resource(UserResource, "/api/v1/user/<int:user_id>", endpoint="user_detail")