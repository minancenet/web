from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from minance.user.models import User

class RegistrationForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired(), Length(min=4, max=16)])
  email = StringField("Email", validators=[DataRequired(), Length(min=6, max=64)])
  password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8, max=128)])
  submit = SubmitField("Sign Up")

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("That username is taken. Please choose a different one.")

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("That email is taken. Please choose a different one.")
    
    if "@" not in email.data:
      raise ValidationError("Not a valid email address.")

class LoginForm(FlaskForm):
  username = StringField("Username", validators=[DataRequired()])
  password = PasswordField("Password", validators=[DataRequired()])
  submit = SubmitField("Login")