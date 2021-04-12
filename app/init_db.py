from app import db
from models import User, recipe_ingredient, Recipe, Ingredient
import os

if os.path.exists('data/recipesite.db'):
  os.remove('data/recipesite.db')

db.create_all()

u1 = User(
  username='testguy1', 
  email='testguy1@test.com'
)
u1.set_password('testpass1')

u2 = User(
  username='testguy2', 
  email='testguy2@test.com'
)
u2.set_password('testpass2')

db.session.add(u1)
db.session.add(u2)

i1 = Ingredient(
  name='Moldy bananas',
  calories_per=50,
  unit_type='gram'
)

db.session.add(i1)

try:
  db.session.commit()
except Exception:
  db.session.rollback()

r1 = Recipe(
  name='Nanners ala Mold',
  instructions='''
1. Pick up moldy banana
2. Shove it in your mouth
3. Question your life choices''',
  source='http://theworstrecipes.com',
  tags='#yuck',
  author=u1,
  ingredients=[i1]
)

db.session.add(r1)

try:
  db.session.commit()
except Exception:
  db.session.rollback()