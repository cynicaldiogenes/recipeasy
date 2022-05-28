import unittest
from app import create_app, db
from app.models import User, Recipe, Ingredient
from config import Config

class TestConfig(Config):
  TESTING = True
  SQLALCHEMY_DATABASE_URI = 'sqlite://'

class UserModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()
    self.app_context.pop()
  
  def test_password_hashing(self):
    u = User(username='susan')
    u.set_password('cat')
    self.assertFalse(u.check_password('dog'))
    self.assertTrue(u.check_password('cat'))
  
  def test_avatar(self):
    u = User(username='john', email='john@example.com')
    self.assertEqual(u.avatar(128),
    ('https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128'))

class RecipeModelCase(unittest.TestCase):
  def setUp(self):
    self.app = create_app(TestConfig)
    self.app_context = self.app.app_context()
    self.app_context.push()
    db.create_all()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

  def test_add_ingredient(self):
    r = Recipe(name='Cereal', instructions='Pour milk in bowl, eat')
    i1 = Ingredient(name='Milk', calories_per=100, unit_type='cup')
    i2 = Ingredient(name='Panda Puffs', calories_per=200, unit_type='cup')
    db.session.add_all([r, i1, i2])
    db.session.commit()

    r.add_ingredient(i1, quantity=5)
    db.session.commit()

    self.assertTrue(r.is_ingredient(i1))
    self.assertFalse(r.is_ingredient(i2))

  def test_remove_ingredient(self):
    r = Recipe(name='Cereal', instructions='Pour milk in bowl, eat')
    i1 = Ingredient(name='Milk', calories_per=100, unit_type='cup')
    i2 = Ingredient(name='Panda Puffs', calories_per=200, unit_type='cup')
    db.session.add_all([r, i1, i2])
    db.session.commit()

    r.add_ingredient(i1, quantity=5)
    r.add_ingredient(i2, quantity=2)
    db.session.commit()

    r.remove_ingredient(i1)
    db.session.commit()

    self.assertFalse(r.is_ingredient(i1))
    self.assertTrue(r.is_ingredient(i2))

if __name__ == '__main__':
  import xmlrunner
  
  unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test_reports'))