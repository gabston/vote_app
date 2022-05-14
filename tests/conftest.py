from flask import Flask
from models import Candidato
from flask_sqlalchemy import SQLAlchemy
import pytest
from handlers.routes.routes_config import api_routes


@pytest.fixture(scope='module')
def new_candidato():
    """
    Creates a new Candidato
    """
    candidato = Candidato(
        num_candidato = "Teste",
        nome='Teste',
        partido='Teste',
        idade='Teste',
        cargo='Teste'
    )
    return candidato

@pytest.fixture(scope='module')
def app():
    app = Flask(__name__, template_folder='../templates/')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"

    db = SQLAlchemy(app)

    api_routes(app)

    return app
    