from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from trade.models import User

class RegistrationForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
  email = StringField("Email", validators=[DataRequired(), Length(min=6, max=64)])
  password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8, max=128)])
  submit = SubmitField("Sign Up")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("That username is taken. Please choose a different one.")

class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")