from database import db
from handlers.routes.routes_config import api_routes
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dbteste.db"
app.secret_key = "AAAAAA"
db.init_app(app)
NoneType = type(None)

api_routes(app)


if __name__ == "__main__":
    app.run()