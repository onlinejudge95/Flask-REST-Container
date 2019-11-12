from flask import Flask, jsonify
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

app.config.from_object("app.config.DevelopmentConfig")


class Ping(Resource):
    @staticmethod
    def get():
        return {"status": "success", "message": "pong!"}


api.add_resource(Ping, "/ping")
