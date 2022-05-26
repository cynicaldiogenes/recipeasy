from app import app, db
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Recipe, Ingredient, RecipeIngredient
from app.forms import LoginForm, RegisterForm, IngredientForm, \
  EditRecipeForm, RecipeIngredientForm, EditProfileForm, EmptyForm
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

@app.route('/recipes/<recipename>')
def recipe(recipename):
  recipe = Recipe.query.filter_by(name=recipename).first_or_404()
  return render_template('recipe.html', recipe=recipe, ingredients=ingredients, title=recipename)

@app.route('/ingredients/<ingredientname>', methods=['GET', 'POST'])
def ingredient(ingredientname):
  ingredient = Ingredient.query.filter_by(name=ingredientname).first_or_404()
  return render_template('ingredient.html', title=f'{ingredientname} details', ingredient=ingredient)

@app.route('/recipes/<recipename>/edit_recipe', methods=['GET', 'POST'])
@login_required
def edit_recipe(recipename):
  recipe = Recipe.query.filter_by(name=recipename).first_or_404()
  form = EditRecipeForm(recipename)
  if form.validate_on_submit():
    recipe.name = form.name.data
    recipe.instructions = form.instructions.data
    recipe.source = form.source.data
    recipe.tags = form.tags.data
    db.session.commit()
    flash(f'{{ recipe.name }} updated.')
  elif request.method == 'GET':
    form.name.data = recipe.name
    form.instructions.data = recipe.instructions
    form.source.data = recipe.source
    form.tags.data = recipe.tags
  return render_template('edit_recipe.html', title=f'Edit {{ recipe.name }}', recipe=recipe, form=form)
    

#Update this route to also set quantity when adding to recipe
@app.route('/recipes/<recipe>/add_recipe_ingredient/<ingredient>', methods=['POST'])
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

@app.route('/recipes/<recipe>/remove_recipe_ingredient/<ingredient>', methods=['POST'])
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

@app.route('/ingredients/add_ingredient', methods=['GET', 'POST'])
@login_required
def add_ingredient():
  form = IngredientForm()
  if form.validate_on_submit():
    ingredient = Ingredient(
      name = form.name.data,
      calories_per = form.calories_per.data,
      unit_type = form.unit_type.data,
      notes = form.notes.data
    )
    db.session.add(ingredient)
    db.session.commit()
    flash(f'Added {ingredient.name}!')
    return redirect(url_for('ingredients'))
  return render_template('add_ingredient.html', title="Add an ingredient", form=form)

@app.route('/recipes/add_recipe', methods=['GET', 'POST'])
@login_required
def add_recipe():
  form = EditRecipeForm(recipename="New Recipe")
  if form.validate_on_submit():
    recipe = Recipe(
      name = form.name.data,
      instructions = form.instructions.data,
      source = form.source.data,
      tags = form.tags.data,
      user_id = current_user.id
    )
    db.session.add(recipe)
    db.session.commit()
    flash(f'Added {recipe.name}!')
    return redirect(url_for('recipes'))
  elif request.method == 'GET':
    form.name.data = "New Recipe"
  return render_template('edit_recipe.html', title="Add a recipe", form=form)