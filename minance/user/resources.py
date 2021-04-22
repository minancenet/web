from flask_restful import Resource, reqparse

from minance.user.models import User
from minance.user.schemas import UserSchema
from minance.api.utils import keyRequired

class UserListResource(Resource):
  def get(self):
    parser = reqparse.RequestParser()
    keyRequired(parser)
    args = parser.parse_args()

    users = User.query.all()
    return UserSchema(many=True).dump(users)

class UserResource(Resource):
  def get(self, user_id):
    parser = reqparse.RequestParser()
    keyRequired(parser)
    args = parser.parse_args()

    user = User.query.get_or_404(user_id)
    return UserSchema().dump(user)