from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired

class TrackForm(FlaskForm):
  purchaseDate = DateField("Purchase Date")
  purchaseTime = TimeField("Purchase Time")

  sellDate = DateField("Sell Date")
  sellTime = TimeField("Sell Time")

  purchaseType = SelectField("Purchase Type", choices=[(0, "Same as Top Order"), (1, "Top Order +0.1"), (2, "5%% of Spread")])
  sellType = SelectField("Sell Type", choices=[(0, "Same as Top Order"), (1, "Top Order +0.1"), (2, "5%% of Spread")])

  reset = SubmitField("Reset")
  check = SubmitField("Check Margins")