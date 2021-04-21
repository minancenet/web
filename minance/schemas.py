from minance import ma
from minance.models import User, Asset

class AssetSchema(ma.Schema):
  class Meta:
    fields = ("name", "lastUpdated", "sellPrice", "buyPrice")
    model = Asset

class UserSchema(ma.Schema):
  class Meta:
    fields = ("username", "email", "_links")
    model = User

  _links = ma.Hyperlinks(
    {
      "self": ma.URLFor("api.user_detail", values=dict(user_id="<id>")),
      "collection": ma.URLFor("api.users"),
    }
  )