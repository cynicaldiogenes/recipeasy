from app import app, db
from flask import request, render_template, flash, redirect, url_for
#from models import User, Recipes, Ingredients, RecipeIngredients, Ratings
#from forms import <all the forms I need to make>
from werkzeug.urls import url_parse

#Landing page
@app.route('/')
def index():
  return render_template("index.html")