import os

from flask import Flask, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

app.config.from_object(os.getenv("APP_SETTINGS"))


class Ping(Resource):
    @staticmethod
    def get():
        return {"status": "success", "message": "pong!"}


api.add_resource(Ping, "/ping")
