from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello world</p>"


@app.route("/two")
def hello_world_two():
    return "<p>Hello world 2</p>"
