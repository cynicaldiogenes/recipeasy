from app import app, db
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recipe, Ingredient, RecipeIngredient
from app.forms import LoginForm, RegisterForm, IngredientForm, RecipeForm, RecipeIngredientForm, EditProfileForm, EmptyForm
from werkzeug.urls import url_parse

@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.route('/')
@app.route('/index')
@login_required
def index():
  return render_template("index.html", title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form=LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first() # update to accept either username or email
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '': #prevent next page from being external link
      next_page = url_for('index')
    return redirect(next_page)
  return render_template('login.html', title="Sign In", form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form=RegisterForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registered a user!')
    return redirect(url_for('login'))
  return render_template('register.html', title="Create an account", form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  recipes = Recipe.query.filter_by(user_id=user.id).all()
  return render_template('user.html', user=user, recipes=recipes)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile', form=form)

@app.route('/recipes')
def recipes():
  recipes = Recipe.query.all()
  return render_template('recipes.html', title='Recipes', recipes=recipes)

@app.route('/ingredients')
def ingredients():
  ingredients = Ingredient.query.all()
  return render_template('ingredients.html', title="Ingredients", ingredients=ingredients)

# Redo this to improve the queries
@app.route('/recipe/<recipename>')
def recipe(recipename):
  recipe = Recipe.query.filter_by(name=recipename).first_or_404()
  ingredients = {}
  for ingredient in recipe.ingredients:
    i = Ingredient.query.filter_by(id=ingredient.ingredient_id).first()
    ingredients[i.name] = ingredient.quantity
  return render_template('recipe.html', recipe=recipe, ingredients=ingredients, title=recipename)

@app.route('/ingredient/<ingredientname>', methods=['GET', 'POST'])
def ingredient(ingredientname):
  ingredient = Ingredient.query.filter_by(name=ingredientname).first_or_404()
  return render_template('ingredient.html', title=f'{ingredientname} details', ingredient=ingredient)

@app.route('/edit_recipe/<recipename>', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipename):
  form = EditRecipeForm()
  recipe = Recipe.query.filter_by(name=recipename).first_or_404()
  if form.validate_on_submit():
    recipe.name = form.name.data
    recipe.instructions = form.instructions.data

@app.route('/add_recipe_ingredient/<recipe>/<ingredient>', methods=['POST'])
@login_required
def add_recipe_ingredient(recipe, ingredient):
  form = EmptyForm()
  if form.validate_on_submit():
    myrecipe = Recipe.query.filter_by(name=recipe).first()
    if myrecipe is None:
      flash(f'Recipe {recipe} not found.')
      return redirect(url_for('index'))
    myingredient = Ingredient.filter_by(name=ingredient).first()
    if myingredient is None:
      flash(f'Ingredient {ingredient} not found.')
    myrecipe.add_ingredient(myingredient)
    db.session.commit()
    flash(f'Added {ingredient} to {recipe}')
    return redirect(url_for('index'))
  else:
    return redirect(url_for('index'))

@app.route('/remove_recipe_ingredient/<recipe>/<ingredient>', methods=['POST'])
@login_required
def remove_recipe_ingredient(recipe, ingredient):
  form = EmptyForm()
  if form.validate_on_submit():
    myrecipe = Recipe.query.filter_by(name=recipe).first()
    if myrecipe is None:
      flash(f'Recipe {recipe} not found.')
      return redirect(url_for('index'))
    myingredient = Ingredient.filter_by(name=ingredient).first()
    if myingredient is None:
      flash(f'Ingredient {ingredient} not found.')
    myrecipe.remove_ingredient(myingredient)
    db.session.commit()
    flash(f'Removed {ingredient} from {recipe}.')
    return redirect(url_for('index'))
  else:
    return redirect(url_for('index'))