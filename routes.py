from app import app, db
from flask import request, render_template, flash, redirect, url_for
#from models import User, Recipes, Ingredients, RecipeIngredients, Ratings
from forms import LoginForm, RegisterForm, IngredientForm, RecipeForm, RecipeIngredientForm
from werkzeug.urls import url_parse

#Landing page
@app.route('/')
@app.route('/index')
def index():
  return render_template("index.html", title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
  form=LoginForm()
  if form.validate_on_submit():
    flash(f'Login requested for user {form.username.data}, remember_me = {form.remember_me.data}.')
    return redirect(url_for('index'))
  return render_template('login.html', title="Sign In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
  form=RegisterForm()
  if form.validate_on_submit():
    flash(f'Creating user {form.username.data} at {form.email.data}! Just kidding, this is a placeholder')
    return redirect(url_for('login'))
  return render_template('register.html', title="Create an account", form=form)