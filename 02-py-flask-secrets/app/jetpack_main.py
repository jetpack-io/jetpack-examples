from flask import Flask
from os import environ
import json

# Import our routes and application code
# Declare a variable "app" with the Flask app
app = Flask(__name__)


@app.route("/")
def hello_world():
    return '<h1>Hello! You are currently in {0}</h1>'.format(
        environ.get("FLASK_ENV"))


@app.route("/readfile")
def read_file():
    f = open('/var/run/secrets/jetpack.io/secrets.json')
    data = json.load(f)
    return data
    

if __name__ == "__main__":
    app.run()
