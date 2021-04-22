from minance import ma
from minance.user.models import User

class UserSchema(ma.Schema):
  class Meta:
    fields = (
      "username",
      "email",
      "_links"
    )

    ordered = True
    model = User

  _links = ma.Hyperlinks(
    {
      "self": ma.URLFor("api.user_detail", values=dict(user_id="<id>")),
      "collection": ma.URLFor("api.users"),
    }
  )