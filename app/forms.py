from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField, SelectMultipleField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError, Length

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

class EditProfileForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
  submit = SubmitField('Submit')

class IngredientForm(FlaskForm):
  name = StringField('Ingredient Name', validators=[DataRequired()]),
  calories_per = IntegerField('Calories per', validators=[DataRequired()]),
  unit_type = StringField('Measurement unit', validators=[DataRequired()]),
  notes = StringField('Notes')
  submit = SubmitField('Add Ingredient')

class RecipeForm(FlaskForm):
  name = StringField('Recipe Name', validators=[DataRequired()]),
  instructions = TextAreaField('Instructions', validators=[DataRequired()]),
  source = URLField('Source')
  submit = SubmitField('Add Recipe')

class RecipeIngredientForm(FlaskForm):
  recipe_ingredients = SelectMultipleField('Ingredients', validators=[DataRequired()])
  quantity = IntegerField('Ingredient Quantity', validators=[DataRequired()])
  submit = SubmitField('Add Ingredients')

  #From https://stackoverflow.com/questions/31619747/dynamic-select-field-using-wtforms-not-updating/31619945#31619945
  def __init__(self, *args, **kwargs):
    super(RecipeIngredientForm, self).__init__(*args, **kwargs)
    self.recipe_ingredients.choices = [ 
      (ingredient.id, ingredient.name) for ingrdient in Ingredient.query.order_by(Ingredient.name)]