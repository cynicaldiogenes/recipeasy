from app import app, db
from flask import request, render_template, flash, redirect, url_for
#from models import User, Recipes, Ingredients, RecipeIngredients, Ratings
from forms import LoginForm
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