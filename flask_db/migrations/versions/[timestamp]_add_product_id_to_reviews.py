from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# This is a command to be run in the terminal, not Python code
# flask db revision --autogenerate -m "add product_id to reviews"
