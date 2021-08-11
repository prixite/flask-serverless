import os
import boto3
import eventlet

from eventlet.green.urllib.request import urlopen
from flask import Flask
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy


host = os.environ.get('DB_HOST')
port = os.environ.get('DB_PORT')
user = os.environ.get('DB_USER')
pwd = os.environ.get('DB_PWD')
db = os.environ.get('DB_NAME')
redis_host = os.environ.get('REDIS_HOST')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{user}:{pwd}@{host}:{port}/{db}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['REDIS_URL'] = redis_host

db = SQLAlchemy(app)
db.init_app(app)

redis_store = FlaskRedis()
redis_store.init_app(app)

BUCKET = 'zappa-oizvh3rit-h'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def index():
    return 'Hello world from Flask'


@app.route('/user')
def user():
    user = User.query.first()
    return f'<h1>User is {user.username}.</h1>'


@app.route('/s3')
def s3():
    s3 = boto3.resource("s3")
    client = boto3.client("s3")
    return f'S3: {s3} <br/> Client: {client}'


@app.route('/s3/upload')
def s3_upload():
    s3 = boto3.resource("s3")
    client = boto3.client("s3")
    file_name = 'file.txt'
    object_name = 'file.txt'
    client.upload_file(file_name, BUCKET, object_name)
    return f'S3: {s3} <br/> Client: {client}'


@app.route('/s3/list')
def s3_list():
    s3 = boto3.resource("s3")
    client = boto3.client("s3")

    files = client.list_objects_v2(Bucket=BUCKET, Prefix='')
    if "Contents" in files:
        return f'{files["Contents"]}'

    return f'{files}'


@app.route('/redis')
def redis():
    client = redis_store._redis_client
    print(client)
    data = dict(redis_store)
    return f'Host: {redis_host} </br> Client: {client} </br> Data: {data}'


@app.route('/redis/set')
def redis_set():
    redis_store.set('token', 'yr982umxytftc898dwscnd8329dwjxn389')
    value = redis_store.get('token')
    return f'OK </br> {value}'


@app.route('/redis/get')
def redis_get():
    value = redis_store.get('dev')
    return f'{value}'


@app.route('/eventlet')
def event():
    gt = eventlet.spawn(urlopen, 'https://fnftxiwh4j.execute-api.us-east-1.amazonaws.com/dev/api/report_4_1/GNVAC/available_total_circuit_size/')
    result = gt.wait()
    return f'{result.getcode()} </br> {result.read()}'
