from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    BooleanField, SubmitField, IntegerField, TextAreaField, \
    SelectMultipleField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import DataRequired, EqualTo, \
    Email, ValidationError, Length, InputRequired
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = EmailField('E-mail address', validators=[DataRequired(), Email()])
  password = PasswordField('Password', 
    validators=[EqualTo('password_confirm', message='Passwords must match')])
  password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
  submit = SubmitField('Register Account')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')
  
  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')