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
  
  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
  
  def __repr__(self):
    return f'User {self.username}'
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

#recipe-ingredient association table
recipe_ingredient = db.Table('recipe_ingredient',
  db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
  db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True),
  db.Column('quantity', db.Integer)
)

#Recipes model
class Recipe(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), index=True, nullable=False, unique=True)
  instructions = db.Column(db.String(5012), nullable=False, unique=False)
  source = db.Column(db.String(128), unique=False)
  tags = db.Column(db.String(128), index=True, unique=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  created = db.Column(db.DateTime(), default=datetime.utcnow)
  ingredients = db.relationship(
    'Ingredient',
    secondary=recipe_ingredient,
    lazy='subquery',
    backref=db.backref('ingredients', lazy=True)
    )

  def __repr__(self):
    return f'Recipe {self.name}'

#Ingredients model
class Ingredient(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64), index=True, nullable=False, unique=True)
  calories_per = db.Column(db.Integer, unique=False)
  unit_type = db.Column(db.String(64), unique=False)
  notes = db.Column(db.String(1024), nullable=True, unique=False)
  created = db.Column(db.DateTime(), default=datetime.utcnow)
  #Commented out the following line because I could only get this working via backref instad of back_populates
  #recipes = db.relationship('Recipe', secondary=recipe_ingredient, back_populates='recipes')

  def __repr__(self):
    return f'Ingredient {self.name}'

#Todo: ratings model
