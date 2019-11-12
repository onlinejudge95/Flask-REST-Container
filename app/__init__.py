import os

from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config.from_object(os.getenv("APP_SETTINGS"))

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class Ping(Resource):
    @staticmethod
    def get():
        return {"status": "success", "message": "pong!"}


api.add_resource(Ping, "/ping")
