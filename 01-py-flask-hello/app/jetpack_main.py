import flask
import json
from pathlib import Path
from flask import Flask
from os import environ

# Import our routes and application code
# Declare a variable "app" with the Flask app
app = Flask(__name__)


@app.route("/")
def hello_world():
    return '<h1>Hello! You are currently in {0}</h1>'.format(
        environ.get("FLASK_ENV"))

if __name__ == "__main__":
    app.run()
