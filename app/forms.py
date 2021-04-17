from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
  BooleanField, SubmitField, IntegerField, TextAreaField, \
  SelectMultipleField
from wtforms.fields.html5 import URLField, EmailField
from wtforms.validators import DataRequired, EqualTo, \
  Email, ValidationError, Length, InputRequired
from app.models import User, Recipe

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

  def __init__(self, original_username, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.original_username = original_username
  
  def validate_username(self, username):
    if username.data != self.original_username:
      user = User.query.filter_by(username=self.username.data).first()
      if user is not None:
        raise ValidationError('Please choose a different username.')  

class IngredientForm(FlaskForm):
  name = StringField('Ingredient Name', validators=[DataRequired()])
  calories_per = IntegerField('Calories per', validators=[InputRequired()])
  unit_type = StringField('Measurement unit', validators=[DataRequired()])
  notes = StringField('Notes')
  submit = SubmitField('Add Ingredient')

class EditRecipeForm(FlaskForm):
  name = StringField('Recipe Name', validators=[DataRequired()])
  instructions = TextAreaField('Instructions', validators=[DataRequired()])
  source = URLField('Source')
  tags = TextAreaField('Tags')
  submit = SubmitField('Save Changes')

  def __init__(self, recipename, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.original_name = recipename
  
  def validate_name(self, name):
    if name.data != self.original_name:
      check_existing_recipe = Recipe.query.filter_by(name=self.name.data).first()
      if check_existing_recipe is not None:
        raise ValidationError(f'A recipe witht this name already exists.')

class RecipeIngredientForm(FlaskForm):
  recipe_ingredients = SelectMultipleField('Ingredients', validators=[DataRequired()])
  quantity = IntegerField('Ingredient Quantity', validators=[DataRequired()])
  submit = SubmitField('Add Ingredients')

  #From https://stackoverflow.com/questions/31619747/dynamic-select-field-using-wtforms-not-updating/31619945#31619945
  def __init__(self, *args, **kwargs):
    super(RecipeIngredientForm, self).__init__(*args, **kwargs)
    self.recipe_ingredients.choices = [ 
      (ingredient.id, ingredient.name) for ingredient in Ingredient.query.order_by(Ingredient.name)]

class EmptyForm(FlaskForm):
  submit = SubmitField('Submit')
