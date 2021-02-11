from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from trade.models import Asset

class AddAssetForm(FlaskForm):
  asset_name = StringField("Asset", validators=[DataRequired()])
  quantity = StringField("Quantity", validators=[DataRequired()])
  submit = SubmitField("Submit")
  
  def validate_asset_name(self, asset_name):
    asset = Asset.query.filter_by(name=asset_name.data).first()
    if not asset:
      raise ValidationError(f"No asset exists named {asset_name.data}.")
