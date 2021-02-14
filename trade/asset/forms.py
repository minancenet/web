from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired

class TrackForm(FlaskForm):
  purchaseDate = DateField("Purchase Date")
  purchaseTime = TimeField("Purchase Time")

  sellDate = DateField("Sell Date")
  sellTime = TimeField("Sell Time")

  reset = SubmitField("Reset")
  check = SubmitField("Check Margins")