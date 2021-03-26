from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, NumberRange

from flask_login import current_user

from minance.models import Asset, User

class PlaceOrderForm(FlaskForm):
  orderType = SelectField("Order Type", choices=[("buy", "Buy"), ("sell", "Sell")], validators=[DataRequired()])
  orderMethod = SelectField("Order Method", choices=[("top_order", "Top Order"), ("top_order_+0.1", "Top Order +0.1"), ("5%_spread", "5% Spread"), ("10%_spread", "10% Spread")], validators=[DataRequired()])
  asset = StringField("Asset Name", validators=[DataRequired()])
  amount = IntegerField("Amount", validators=[DataRequired(), NumberRange(min=1)])
  fee = SelectField("Fee", choices=[(0.1, "0.1%"),
                                    (0.2, "0.2%"),
                                    (0.3, "0.3%"),
                                    (0.4, "0.4%"),
                                    (0.5, "0.5%"),
                                    (0.75, "0.75%"),
                                    (1, "1%"),
                                    (2, "2%"),
                                    (3, "3%"),
                                    (4, "4%"),
                                    (5, "5%"),
                                    (7.5, "7.5%")
                            ], validators=[DataRequired()])
  minimumTrust = SelectField("Trust", choices=[(0, "0"),
                                                      (1, "1"),
                                                      (2, "2"),
                                                      (3, "3"),
                                                      (4, "4"),
                                                      (5, "5"),
                                                      (6, "6"),
                                                      (7, "7"),
                                                      (8, "8"),
                                                      (9, "9"),
                                                      (10, "10")
                              ], validators=[DataRequired()])
  visibility = SelectField("Visibility", choices=[("private", "Private"), ("public", "Public")], validators=[DataRequired()])

  place = SubmitField("Place Order")

  def validate_asset(self, asset):
    # asset = Asset.query.filter_by(name=(asset.data).capitalize().replace(" ", "_")).first()
    asset = Asset.query.filter_by(name="STOCK_OF_STONKS").first()
    if not asset:
      raise ValidationError("There is no asset with this name.")

class UpdateAccountForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  email = StringField("Email", validators=[DataRequired()])
  biography = TextAreaField("Biography")
  discord = StringField("Discord", validators=[DataRequired()])

  update = SubmitField("Update")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user and user != current_user:
      raise ValidationError("That username is taken. Please choose a different one.")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user and user != current_user:
      raise ValidationError("That email is taken. Please choose a different one.")