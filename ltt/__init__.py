from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.db'
app.config['SECRET_KEY'] = '665effa02d70007ef16b81c5a369cda8'
db = SQLAlchemy(app)  #db object
from ltt import models

#register buleprint
from .view import view
app.register_blueprint(view,url_prefix='/')

