from flask import request, render_template, flash, redirect, url_for
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegisterForm
from app.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form=LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first() # update to accept either username or email
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('auth.login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '': #prevent next page from being external link
      next_page = url_for('main.index')
    return redirect(next_page)
  return render_template('auth/login.html', title="Sign In", form=form)

@bp.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.index'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.index'))
  form=RegisterForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Registered a user!')
    return redirect(url_for('auth.login'))
  return render_template('auth/register.html', title="Create an account", form=form)