from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://admin:nightduty@umair-g1-test-db.cse78obf8zdr.us-east-1.rds.amazonaws.com:3306/gpns"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return 'Hello world from Flask'


@app.route('/cat')
def cat():
    return 'Cat'


@app.route('/user')
def user():
    user = User.query.first()
    return f'<h1>User is {user.username}.</h1>'
