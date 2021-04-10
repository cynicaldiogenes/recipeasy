from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)


#create login manager later
login_manager = LoginManager()
login_manager.init_app(app)
import routes
#import models later