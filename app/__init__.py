from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Check database connection
try:
    with app.app_context():
        db.create_all()  # Try to create a table to check the connection
    print("Database connection successful!")
except Exception as e:
    print("Error connecting to the database:", str(e))
    raise e  # Raising the exception to stop the application startup

from app import models, views
