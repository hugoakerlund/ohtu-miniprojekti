from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import getenv

load_dotenv()

test_env = getenv("TEST_ENV") == "true"
print(f"Test environment: {test_env}")

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
db_url = getenv("DATABASE_URL")

if db_url and db_url.startswith("sqlite:///"):
    path = db_url.replace("sqlite:///", "", 1)
    if not path.startswith("/"):
        db_url = "sqlite:////tmp/" + path

app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db = SQLAlchemy(app)
