from flask import Flask
from pytest import param

def create_app():
    app = Flask(__name__, template_folder='../templates/')
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dbteste.db"
    app.secret_key = "AAAAAA"
    return app