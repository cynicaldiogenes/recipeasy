from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

#User Loader
@login.user_loader
def load_user(id):
  return User.query.get(int(id))

#User model
class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, nullable=False, unique=True)
  email = db.Column(db.String(120), index=True, nullable=False, unique=True)
  password_hash = db.Column(db.String(128))
  created = db.Column(db.DateTime(), default=datetime.utcnow)
  recipes = db.relationship('Recipe', backref='author', lazy='dynamic')
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  
  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
  
  def __repr__(self):
    return f'User {self.username}'
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

#recipe-ingredient association table via model
class RecipeIngredient(db.Model):
  recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
  ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
  quantity = db.Column(db.Float)
  recipe = db.relationship('Recipe', back_populates='ingredients')
  ingredient = db.relationship('Ingredient', back_populates='recipes')

#Recipes model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), index=True, nullable=False, unique=True)
  instructions = db.Column(db.String(5012), nullable=False, unique=False)
  source = db.Column(db.String(128), unique=False)
  tags = db.Column(db.String(128), index=True, unique=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  created = db.Column(db.DateTime(), default=datetime.utcnow)
  ingredients = db.relationship('RecipeIngredient', back_populates='recipe', cascade="save-update, merge, delete, delete-orphan")

  def __repr__(self):
    return f'Recipe {self.name}'
  
  def add_ingredient(self, ingredient, quantity=1):
    if not self.is_ingredient(ingredient):
      self.ingredients.append(
        RecipeIngredient(recipe_id=self.id, ingredient_id=ingredient.id, quantity=quantity))

  def remove_ingredient(self, ingredient):
    if self.is_ingredient(ingredient):
      self.ingredients.remove(RecipeIngredient.query.filter(
        RecipeIngredient.ingredient_id == ingredient.id,
        RecipeIngredient.recipe_id == self.id).first())

  def is_ingredient(self, ingredient):
    if RecipeIngredient.query.filter(
      RecipeIngredient.ingredient_id == ingredient.id, 
      RecipeIngredient.recipe_id == self.id).first():
      return True

#Ingredients model
class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, nullable=False, unique=True)
  calories_per = db.Column(db.Integer, unique=False)
  unit_type = db.Column(db.String(64), unique=False)
  notes = db.Column(db.String(1024), nullable=True, unique=False)
  created = db.Column(db.DateTime(), default=datetime.utcnow)
  recipes = db.relationship('RecipeIngredient', back_populates='ingredient')

  def __repr__(self):
    return f'Ingredient {self.name}'