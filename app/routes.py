from app import app, db
from datetime import datetime
from flask import request, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User#, Recipes, Ingredients, RecipeIngredients, Ratings
from app.forms import LoginForm, RegisterForm, IngredientForm, RecipeForm, RecipeIngredientForm, EditProfileForm
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
  recipes = [
    {'author': user, 'name': 'test recipe #1'},
    {'author': user, 'name': 'test recipe #2'}
  ]
  return render_template('user.html', user=user, recipes=recipes)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title="Edit Profile", form=form)