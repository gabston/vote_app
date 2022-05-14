from flask import Flask
from handlers.routes.routes_config import api_routes

def test_get_page():
    app = Flask(__name__)
    api_routes(app)
    client = app.test_client()
    url = '/'
    response = client.get(url)
    assert response.status_code == 200